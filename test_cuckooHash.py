import pytest
import random
from CuckooHash import CuckooHash


def test_randomInsert():
    c = CuckooHash(10)
    inserted = []
    for i in range(random.randint(0,100)):           #loop upto a 100 times
        x = random.randint(0,100)                    #get a random int upto 100
        if not (x in inserted):                      #this list is to keep track of what is supposed to be inserted (no duplicates)
            inserted.append(x)
        c.insert(str(x), str(x))                     #try to insert x in the CuckooHash(should not insert duplicates)
    assert len(inserted) == len(c)                   #the length of the list and the CuckooHash should be the same
    
    
def test_insertingAll():                             #Insert the numbers from 0 to 99, the final length should be 100
    c = CuckooHash(100)                            
    for i in  range(100):
        c.insert(str(i), str(i))
    assert len(c) == 100


def test_noDuplicates():                             #Insert 20 times the same key
    c = CuckooHash(20)
    for i in range(20):
        c.insert("A", str(i))
    assert c.find("A") == "0"                        #it should return the data of the first inserted
    c.delete("A")                                    #After deleting("A"), if we try to find it, we shouldn't be able to because we dont have duplicates
    assert c.find("A") == None                       #return None if it wasn't there
    

def test_empty():                                    #cant find or delete something on an empty CuckooHash
    c = CuckooHash(20)
    assert c.find("A") == None                       
    assert c.delete("A") == False
    assert len(c) ==  0
    
    
def test_delete():                                   #Insert numbers from 0 to 19
    c = CuckooHash(1000)
    for i in range(20):
        c.insert(str(i), str(i))
    assert len(c) == 20                              #the length should be 20
    for i in range(10):
        c.delete(str(i))                             #Delete the numbers upto 9.
    assert len(c) == 10                              #the final length should be 10


def test_allThere():                                 #after inserting elements we should be able to find them all. 
    c = CuckooHash(10)                               #Since the initial size is 10 and we are inserting 50 elements, if it pass this test, __growHash works
    lost = 0
    for i in range(50):                              
        c.insert(str(i), str(i))
    for i in range(50):
        if c.find(str(i)) == None:
            lost +=1
    assert lost == 0
    
    
def test_grow():                                     #After inserting 3 elements the array should grow because the numOfRecords>=numOfBuckets
    c = CuckooHash(6)
    c.insert("A", "a")
    c.insert("B", "b")
    c.insert("C", "c")
    assert c.numOfBuckets() == 12

    
        
pytest.main(["-v", "-s"])
