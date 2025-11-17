import io
import csv
from database.base import SessionLocal
from database.models import User, Question, UserAnswer
from sqlalchemy import func

def generate_stats_csv():
    """Генерирует CSV файл с подробной статистикой."""
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    
    with SessionLocal() as session:
        # Заголовки: ФИО, Класс, Вопрос 1, Вопрос 2 ... Итого
        questions = session.query(Question).order_by(Question.question_id).all()
        headers = ["ФИО", "Класс"] + [f"В{i+1}: {q.question_text[:15]}..." for i, q in enumerate(questions)] + ["Верно", "Результат %"]
        writer.writerow(headers)
        
        users = session.query(User).all()
        
        for user in users:
            row = [user.full_name, user.class_name]
            correct_count = 0
            
            # Собираем ответы пользователя
            user_answers_map = {} # question_id -> chosen_option
            answers = session.query(UserAnswer).filter(UserAnswer.user_id == user.user_id).all()
            for ans in answers:
                user_answers_map[ans.question_id] = ans
                if ans.is_correct:
                    correct_count += 1
            
            # Заполняем колонки по вопросам
            for q in questions:
                ans_obj = user_answers_map.get(q.question_id)
                if ans_obj:
                    val = getattr(q, f"option_{ans_obj.chosen_option}")
                    row.append(val)
                else:
                    row.append("-")
            
            # Итоги
            total_q = len(questions)
            percent = round((correct_count / total_q) * 100, 1) if total_q > 0 else 0
            row.append(correct_count)
            row.append(f"{percent}%")
            
            writer.writerow(row)
            
    output.seek(0)
    return output
