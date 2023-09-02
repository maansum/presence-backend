

import random 
def check_attendance(group_image_path, student_images):
    shuffled_array = random.sample(student_images, len(student_images))
    return shuffled_array[0 : (len(student_images)//2) ]


# # print(os.path.abspath("./"))
