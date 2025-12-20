donatians= {
    "jadi": 30,
    "sara":45,
    "hossein":43,
    "Ali":399,
}

def donations_calculater(donats):
    total= 0
    average =0

    for donate in donats.values():
        total+=donate
    max_person=max(donats.values())
    average=total/len(donats)   
    return total,max_person,average

print(donations_calculater(donatians))