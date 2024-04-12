import pickle

while True:
    try:
        with open('doneTF', 'rb') as f:
            done = pickle.load(f)
            print(done)
            print("yipee")
    except:
        done = False
        print("failed")
    