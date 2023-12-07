from datetime import date, datetime, timedelta
from collections import defaultdict


def get_birthdays_per_week(users):
   
    group_week = defaultdict(list)

    today = date.today()
    if len(users) == 0:
        
        return group_week
    
    for day in range(7):
        current_day = today + timedelta(days=day)
        

        for dict_user in users:
            birthday = dict_user["birthday"]
            
            
            if birthday.month == current_day.month and birthday.day == current_day.day:
                day_week = current_day.strftime("%A")
                
                if current_day.weekday() == 6:
                    group_week['Monday'].append(dict_user["name"].split(' ')[0])
                elif current_day.weekday() == 5:
                    group_week['Monday'].append(dict_user["name"].split(' ')[0])
                else:
                    group_week[day_week].append(dict_user["name"].split(' ')[0])
                    
                    print(group_week)
        
            
    return group_week
                


if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(1976, 12, 10).date()},
    ]

    result = get_birthdays_per_week(users)
    print(result)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
