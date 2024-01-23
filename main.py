import argparse
from models import Teacher, Group, Student, Subject, Grade, database_url
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine(database_url)
Session = sessionmaker(bind=engine)


def create_model(**kwargs):
    session = Session()

    new_object = None

    if kwargs.get('model') == 'Teacher':
        new_object = Teacher(name=kwargs.get('name'))

    elif kwargs.get('model') == 'Group':
        new_object = Group(name=kwargs.get('name'))

    elif kwargs.get('model') == 'Student':
        new_object = Student(name=kwargs.get('name'), group_id=kwargs.get('group_id'))

    elif kwargs.get('model') == 'Subject':
        new_object = Subject(name=kwargs.get('name'), teacher_id=kwargs.get('teacher_id'))

    elif kwargs.get('model') == 'Grade':
        new_object = Grade(student_id=kwargs.get('student_id'), subject_id=kwargs.get('subject_id'), grade=kwargs.get('grade'))

    if new_object:
        session.add(new_object)
        session.commit()
        print(f"{kwargs.get('model')} created.")
    else:
        print(f"Can not create {kwargs.get('model')} with this params")


def list_models(model_name):
    session = Session()

    model_classes = models_array

    model_class = model_classes.get(model_name)

    if model_class:
        items = session.query(model_class).all()
        for item in items:
            print(f"{model_name} ID: {item.id}, Name: {getattr(item, 'name', 'N/A')}")
    else:
        print(f"Model '{model_name}' not find")


def update_model(model_name, model_id, **kwargs):
    session = Session()

    if model_name == 'Teacher':
        item = session.query(Teacher).filter_by(id=model_id).first()
        if item and 'name' in kwargs:
            item.name = kwargs['name']

    elif model_name == 'Group':
        item = session.query(Group).filter_by(id=model_id).first()
        if item and 'name' in kwargs:
            item.name = kwargs['name']

    elif model_name == 'Student':
        item = session.query(Student).filter_by(id=model_id).first()
        if item:
            if 'name' in kwargs:
                item.name = kwargs['name']
            if 'group_id' in kwargs:
                item.group_id = kwargs['group_id']

    elif model_name == 'Subject':
        item = session.query(Subject).filter_by(id=model_id).first()
        if item:
            if 'name' in kwargs:
                item.name = kwargs['name']
            if 'teacher_id' in kwargs:
                item.teacher_id = kwargs['teacher_id']

    elif model_name == 'Grade':
        item = session.query(Grade).filter_by(id=model_id).first()
        if item:
            if 'student_id' in kwargs:
                item.student_id = kwargs['student_id']
            if 'subject_id' in kwargs:
                item.subject_id = kwargs['subject_id']
            if 'grade' in kwargs:
                item.grade = kwargs['grade']

    if item:
        session.commit()
        print(f"{model_name} (ID: {model_id}) update.")
    else:
        print(f"{model_name} with ID {model_id} not find or bad params.")


def remove_model(model_name, model_id):
    session = Session()

    model_classes = models_array

    model_class = model_classes.get(model_name)

    if model_class:
        item = session.query(model_class).filter_by(id=model_id).first()
        if item:
            session.delete(item)
            session.commit()
            print(f"{model_name} (ID: {model_id}) deleted.")
        else:
            print(f"{model_name} with ID {model_id} not find.")
    else:
        print(f"Model '{model_name}' not find.")


def parse_command(args):
    action = args.action
    model = args.model
    model_id = args.id
    name = args.name

    if action == 'create' and name:
        create_model(model=model, name=name)
    elif action == 'list':
        list_models(model)
    elif action == 'update' and model_id and name:
        update_model(model, model_id, name=name)
    elif action == 'remove' and model_id:
        remove_model(model, model_id)
    else:
        print("Bad agriment")


commands_array = {
    'create',
    'list',
    'update',
    'remove'
    }

models_array = {
        'Teacher': Teacher,
        'Group': Group,
        'Student': Student,
        'Subject': Subject,
        'Grade': Grade
    }

def main():
    parser = argparse.ArgumentParser(description='CLI для взаємодії з базою даних.')
    parser.add_argument('-a', '--action', choices=commands_array, required=True)
    parser.add_argument('-m', '--model', choices=models_array.keys(), required=True)
    parser.add_argument('-n', '--name', type=str)
    parser.add_argument('-id', '--id', type=int)

    args = parser.parse_args()
    parse_command(args)


if __name__ == '__main__':
    main()
