# def create_room(room_name, *args, **kwargs):
#   print(f"These are the stats for {room_name}")
  
#   for key, value in kwargs.items():
    
#     print(f"* {key} -> {value} ")
    
# room_name =input("Enter the Room name: ") 

# kwargs={}
# while True:
#   key = input("Enter the key or done if you already did: ")
#   if key.lower() == "done":
#     break
  
#   value = input("Enter the value for the key: ")
  
#   kwargs[key] = value
# create_room(room_name, **kwargs)
  
  
#none as a data type
def user(name: str | None = None):
  if name is not None:
    print(f"Hello {name}!")
    
  else:
    print("No name provided")
    
user("John")



#class as a data type
class Person:
  def __init__(self,name:str):
    self.name=name
def get_name(person:Person):
  return person.name

__