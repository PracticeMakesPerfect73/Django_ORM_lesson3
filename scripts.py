from datacenter.models import (Chastisement, Commendation, Lesson,
                               Mark, Schoolkid)
from random import choice

COMMENDATION_TEXTS = [
    "Молодец!", "Отлично!", "Хорошо!", "Гораздо лучше, чем я ожидал!",
    "Ты меня приятно удивил!", "Великолепно!", "Прекрасно!",
    "Ты меня очень обрадовал!", "Талантливо!", "Я поражен!"
]


def fix_marks(schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__lte=3).update(points=5)


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid, subject_title):
    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title__contains=subject_title
    ).order_by('-date').first()

    if not lesson:
        print(f"Занятия по предмету '{subject_title}' не найдены.")
        return

    Commendation.objects.create(
        text=choice(COMMENDATION_TEXTS),
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher
    )


def find_schoolkid(full_name):
    schoolkids = Schoolkid.objects.filter(full_name__contains=full_name)
    if not schoolkids:
        print(f"Ученик с именем '{full_name}' не найден.")
        return
    if schoolkids.count() > 1:
        print(f"Найдено несколько учеников с именем '{full_name}':")
        return
    else:
        return schoolkids.first()


def main():
    kid_full_name = input("Введите полное имя ученика: ")
    subject_title = input("Введите название предмета: ")
    schoolkid = find_schoolkid(kid_full_name)
    if schoolkid:
        fix_marks(schoolkid)
        remove_chastisements(schoolkid)
        create_commendation(schoolkid, subject_title)


if __name__ == '__main__':
    main()
