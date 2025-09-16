from cs.models import ComputerScienceConcept, FieldOfStudy
from django.utils.text import slugify
from django.db.utils import IntegrityError

print("Начинаем наполнение базы данных тестовыми концепциями...")

# Если у вас нет созданных FieldOfStudy, создайте хотя бы одну
field = FieldOfStudy.objects.first()

if not field:
    # Создадим область по умолчанию, если ее нет
    field, created = FieldOfStudy.objects.get_or_create(name="Общие концепции CS", defaults={'description': 'Основные концепции компьютерных наук'})
    if created:
        print(f"Создана новая область науки: {field.name}")
    else:
        print(f"Используется существующая область науки: {field.name}")
else:
    print(f"Используется существующая область науки: {field.name}")

concepts_added_count = 0
for i in range(1, 21):
    title = f"Тестовая концепция {i}"
    try:
        concept, created = ComputerScienceConcept.objects.get_or_create(
            title=title,
            defaults={
                'slug': slugify(title),
                'description': f"Описание тестовой концепции компьютерных наук номер {i}.",
                'difficulty': (i % 5) + 1, # Сложность от 1 до 5
                'is_published': ComputerScienceConcept.Status.PUBLISHED,
                'field_of_study': field
            }
        )
        if created:
            concepts_added_count += 1
            print(f"Добавлена концепция: {concept.title}")
        else:
            print(f"Концепция уже существует, пропускаем: {concept.title}")
    except IntegrityError as e:
        print(f"Ошибка при добавлении концепции '{title}': {e}. Возможно, слаг уже существует.")
        # Попытка создать уникальный слаг, если проблема в нем
        base_slug = slugify(title)
        num = 1
        while ComputerScienceConcept.objects.filter(slug=f"{base_slug}-{num}").exists():
            num += 1
        try:
            ComputerScienceConcept.objects.create(
                title=title,
                slug=f"{base_slug}-{num}",
                description=f"Описание тестовой концепции компьютерных наук номер {i}.",
                difficulty=(i % 5) + 1,
                is_published=ComputerScienceConcept.Status.PUBLISHED,
                field_of_study=field
            )
            concepts_added_count += 1
            print(f"Добавлена концепция (с новым слагом): {title}")
        except Exception as inner_e:
            print(f"Повторная ошибка при добавлении концепции '{title}': {inner_e}")


print(f"Завершено. Всего добавлено новых концепций: {concepts_added_count}.")
