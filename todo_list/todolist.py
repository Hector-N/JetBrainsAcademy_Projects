from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
BaseClass = declarative_base()


class TaskTable(BaseClass):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.now().date())

    def __repr__(self):
        return self.task


BaseClass.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
make_schedule = Session()


def add_task():

    task_description = input('\nEnter task').strip()

    while True:
        deadline_str = '-'.join(input('Enter deadline, yyyy-mm-dd: ').strip().split())  # YYYY-MM-DD
        if not deadline_str:
            break
        elif re.search(r"\d\d\d\d-\d\d-\d\d", deadline_str):
            break
        else:
            print("Wrong date format. Repeat, please...")

    if deadline_str:
        task_deadline = datetime.strptime(deadline_str, '%Y-%m-%d')  # strPOSTtime
        new_task = TaskTable(task=task_description,
                             deadline=task_deadline)
    else:
        new_task = TaskTable(task=task_description)

    make_schedule.add(new_task)
    make_schedule.commit()
    print('The task has been added!\n')


def show_tasks(trigger=None, delete=False):
    if trigger == 'all':
        tasks = make_schedule.query(TaskTable).order_by(TaskTable.deadline).all()

        if not tasks:
            if not delete:
                print('Nothing to do!\n')
        else:
            records = (f"{n}. {r.task}. {r.deadline.day} {r.deadline.strftime('%b')}"
                       for n, r
                       in enumerate(tasks, start=1))

            if not delete:
                # for n, record in enumerate(tasks, start=1):
                #     print(f"{n}. "
                #           f"{record.task}. "
                #           f"{record.deadline.day} {record.deadline.strftime('%b')}")
                #     f"{record.deadline.strftime('%d %b')}")
                print('\nAll tasks:')
                for r in records:
                    print(r)
                print()

            elif delete is True:
                print('\nChoose the number of the task you want to delete:')
                for r in records:
                    print(r)
                number_from_list = int(input().strip())

                records_dict = dict(enumerate(tasks, start=1))
                id_task_to_delete = records_dict[number_from_list].id
                task_to_delete = make_schedule.query(TaskTable)\
                                .filter(TaskTable.id == id_task_to_delete)\
                                .all()[0]
                make_schedule.delete(task_to_delete)
                make_schedule.commit()
                print('The task has been deleted!\n')

    elif trigger == 'today':
        date_py = datetime.today().date()
        tasks = make_schedule.query(TaskTable)\
                .filter(TaskTable.deadline == date_py)\
                .order_by(TaskTable.deadline)\
                .all()
        print(f"\nToday {date_py.strftime('%d %b')}:")

        if not tasks:
            print('Nothing to do!\n')
        else:
            for n, record in enumerate(tasks, start=1):
                print(f"{n}. "
                      f"{record.task}")
            print()

    elif trigger == 'week':
        date_py = datetime.today().date()
        print()
        for _i in range(7):
            tasks = make_schedule.query(TaskTable). \
                filter(TaskTable.deadline == date_py). \
                order_by(TaskTable.deadline).all()
            print(f"{date_py.strftime('%A %d %b')}:")

            if not tasks:
                print('Nothing to do!\n')
            else:
                for n, t in enumerate(tasks, start=1):
                    print(f"{n}. {t}")
                print()
            date_py = date_py + timedelta(days=1)

    elif trigger == 'missed':
        print('\nMissed tasks:')
        today = datetime.now().date()
        missed_tasks = make_schedule.query(TaskTable). \
            filter(TaskTable.deadline < today). \
            order_by(TaskTable.deadline).all()

        if missed_tasks:
            for n, record in enumerate(missed_tasks, start=1):
                print(f"{n}. {record.task}. {record.deadline.day} {record.deadline.strftime('%b')}")
            print()
        else:
            print('Nothing is missed!\n')


def quit_ui():
    print('\nBye!')


# ---------- user interface -----------

menu_list = ["1) Today's tasks",
             "2) Week's tasks",
             "3) All tasks",
             "4) Missed tasks",
             "5) Add task",
             "6) Delete task",
             "0) Exit"]
menu_string = '\n'.join(menu_list)

while True:
    print(menu_string)
    action = int(input().strip())
    if action == 1:
        show_tasks('today')

    elif action == 2:
        show_tasks('week')

    elif action == 3:
        show_tasks('all')

    elif action == 4:
        show_tasks('missed')

    elif action == 5:
        add_task()

    elif action == 6:
        show_tasks('all', delete=True)

    elif action == 0:
        quit_ui()
        break
