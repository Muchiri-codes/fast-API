# def create_user(name, *args):
#   specifics = ', '.join(args)
#   print(name, specifics)
  
# create_user("John", '24 years', 'old enough', 'was here')

def tell_more(name:str, age:int):
  details = name + "is this old:" +str(age)
  return details

print(tell_more("john", 34))