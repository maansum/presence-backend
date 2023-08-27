import random 
def check_attendance(group_image_path, student_images):
    shuffled_array = random.sample(student_images, len(student_images))
    return shuffled_array[0 : (len(student_images)//2) ]

# print(check_attendance("files/group.jpg", ['files/1.jpg', 'files/2.jpg', 'files/4.jpg', 'files/5.jpg', 'files/6.jpg', 'files/7.jpg']))
