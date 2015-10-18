from pushbullet import Pushbullet

pb = Pushbullet("bYJFjyvIYWbn5vg2eNiFmcapjLu1PUTL")

push = pb.push_note("This is the title", "This is the body")

with open(r"C:\Workspace\2.png", "rb") as pic:
    file_data = pb.upload_file(pic, "picture.jpg")
push = pb.push_file(**file_data)
pushes = pb.get_pushes()