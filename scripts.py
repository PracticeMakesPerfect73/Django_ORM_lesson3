from datacenter.models import (Chastisement, Commendation, Lesson,
                               Mark, Schoolkid)
from random import choice


def fix_marks(schoolkid):
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__lte=3)
    for bad_mark in bad_marks:
        bad_mark.points = 5
        bad_mark.save()


def remove_chastisements(schoolkid):
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisements.delete()


def create_commendation(schoolkid, subject_title):
    lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title__contains=subject_title
    )
    lesson = choice(lessons)
    commendation_texts = [
        "Молодец!", "Отлично!", "Хорошо!", "Гораздо лучше, чем я ожидал!",
        "Ты меня приятно удивил!", "Великолепно!", "Прекрасно!",
        "Ты меня очень обрадовал!", "Талантливо!", "Я поражен!"
    ]
    Commendation.objects.create(
        text=choice(commendation_texts),
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher
    )


def find_schoolkid(full_name):
    schoolkids = Schoolkid.objects.filter(full_name__contains=full_name)
    if schoolkids.count() == 0:
        print(f"Ученик с именем '{full_name}' не найден.")
        return None
    elif schoolkids.count() > 1:
        print(f"Найдено несколько учеников с именем '{full_name}':")
        for kid in schoolkids:
            print(kid.full_name)
        return None
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
