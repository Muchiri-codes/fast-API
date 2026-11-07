#CLASS - its an object constructor

# class MyClass:
#   age=23
#   state= 4
  
  
# def Me (MyClass):
#   print(MyClass.age, MyClass.state)
  
# Me(MyClass)


# class Student:
#   name="John"
#   age=24

  
#   #self refers to the current object  and its used to store data inside it
#   def __init__(self, year, location, gender):
#     self.year=year
#     self.location=location
#     self.gender = gender
    
# john = Student(4, "Kiamaina", "Male")

# print(john.name, john.age, john.year, john.gender, john.location)





#__str__()  - used to define a custom string representation of an object



class Car:
  def __init__(self, model, age):
    self.model = model        
    self.age = age
    
  def __str__(self):
      return f"{self.model} was first released in the year '45' and is now {self.age} years old."
    
mustang = Car("Toyota Corolla", 5)
hilux = Car("Toyota hilux", 6)

print(mustang)
print(hilux)