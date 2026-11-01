def create_room(room_name, **kwargs):
  print(f'{room_name} Statistics')
  for key, value in kwargs.items():
    print(f"* {key} -> {value}")
    
create_room("Kitchen", lights="off", age=34, price=545800)
create_room("Laboratory", isActice='Yes',age=6 )
    
#kwargs allow one to input dictionary as extra values 
# the double asterics is what determines that irs a dictionary ie key, value pairs