from BitHash import BitHash, ResetBitHash
import time

class Node(object):
    def __init__(self, k, d):
        self.key = k
        self.data = d

class CuckooHash(object):
    def __init__(self, size):
        self.__nestArray1 = [None] * (size//2)                                 #create 2 arrays with half of the size of the CuckooHash
        self.__nestArray2= [None] * (size//2)
        self.__numBuckets = size                                               #total number of buckets
        self.__numRecords = 0                                                  #count of inserted keys
        
    def __str__(self):                                                         #String representation of the cuckoo hash
        ans = "Table 1: "
        for bucket in self.__nestArray1:
            if bucket:
                ans += bucket.key + "-" + str(bucket.data) + " "
        ans +="\nTable 2: "
        for bucket in self.__nestArray2:
            if bucket:
                ans += bucket.key + "-" + str(bucket.data) + " "
        return ans
    
    def __len__(self):                                                         #returns the number of inserted nodes
        return self.__numRecords
    
    def numOfBuckets(self):                                                    #returns the number of buckets in the CuckooHash, created to do some tests later
        return self.__numBuckets
    
    def __findBuckets(self, k):
        hash1 = BitHash(k)                                                     #this is the first hash function
        bucket1 = hash1 % self.__numBuckets//2                                 #this calculates the location of the key in the first array
        bucket2 = BitHash(k, hash1) % int(self.__numBuckets//2)                #this calculates the location of the key in the second array
        return (bucket1, bucket2)                                              #returns the nests that belong to the specified key
        
    def find(self, k):
        nest1, nest2 = self.__findBuckets(k)     
        if self.__nestArray1[nest1] and self.__nestArray1[nest1].key == k:     #if the key is in the first nest
            return self.__nestArray1[nest1].data                               #return data
        elif self.__nestArray2[nest2] and self.__nestArray2[nest2].key == k:   #otherwise, if is in the second  possible nest
            return self.__nestArray2[nest2].data                               #return data
                                                                               #return None if the key wasn't found

    def delete(self, k):
        nest1, nest2 = self.__findBuckets(k)
        if self.__nestArray1[nest1] and self.__nestArray1[nest1].key == k:     #if the key is in the first nest
            self.__nestArray1[nest1] = None                                    #remove key/data pair by setting it to None         
            self.__numRecords -= 1                                             #reduce the number of elements
            return k                                                           #return the deleted key
        elif self.__nestArray2[nest2] and self.__nestArray2[nest2].key == k:   #otherwise, if is in the second  possible nest
            self.__nestArray2[nest2] = None                                    #remove key/data pair by setting it to None
            self.__numRecords -= 1                                             #reduce the number of elements
            return k                                                           #return the deleted key
        return False                                                           #return False if the key wasn't deleted
    
    def __growHash(self):                                                      
        self.__numBuckets = self.__numBuckets * 2                              #double the size of the CuckooHash
        self.rehash()                                                          #relocate the existent key/data pairs
    
    def rehash(self):   
        ResetBitHash()                                                         #Use 2 new Hash functions
        oldArray1 = self.__nestArray1                                          #Create two new hash arrays that are the copy of the old ones
        oldArray2 = self.__nestArray2
        
        arraysSize = self.__numBuckets//2                                      #calculate the length of each table
        self.__nestArray1 = [None] * arraysSize                                #Erase the original arrays
        self.__nestArray2 = [None] * arraysSize
        self.__numRecords = 0
        
        for i in range(len(oldArray1)):                                        #loop through the old array and insert them in a different way(new hash functions)
            if oldArray1[i] != None:                                           #insert what is in the ith position of the first old array
                self.insert(oldArray1[i].key, oldArray1[i].data)
            if oldArray2[i] != None:                                           #insert what is in the ith position of the second old array
                self.insert(oldArray2[i].key, oldArray2[i].data)
            
              
    def insert(self, k, d, resetBitHash = False, count = 0):
        if self.find(k):                                                       #If the key already exists
            return False                                                       #return False
            
        node = Node(k,d)                                                       #create a new node
    
        nest1, nest2 = self.__findBuckets(node.key)                            #find the two possible nests
      
        threshold = 5                                                          #this is the maximum number of evictions
        
        if self.__nestArray1[nest1] == None:                                   #If nest 1 is empty
            self.__nestArray1[nest1] = node                                    #insert it there
            self.__numRecords += 1                                             #increment the count
            if self.__numRecords>=0.5*self.__numBuckets:                       #if the numOfRecords is half of the number of buckets
                self.__growHash()     
            return True
        elif self.__nestArray2[nest2] == None:                                 #If nest1 is ocuppied and nest 2 is empty
            self.__nestArray2[nest2] = node                                    #insert it there
            self.__numRecords += 1                                             #increment the count
            if self.__numRecords>=0.5*self.__numBuckets:                       #if the numOfRecords is half of the number of buckets
                self.__growHash()     
            return True
            
        node, self.__nestArray1[nest1] = self.__nestArray1[nest1], node        #evict occupant
        count +=1                                                              #evicted so far
        
        if count == threshold and resetBitHash ==  False:                      #if is the first infinite loop
            self.rehash()                                                      #use two new functions and rehash everything
            resetBitHash = True                                                #flag to mark that we already called ResetBitHash once
            count = 0                                                          #restart the counting of evictions
        elif (count == threshold and resetBitHash == True) or (self.__numRecords>=0.5*self.__numBuckets): #If we already fell in an infinity loop once or if the numOfRecords is half of the number of buckets
            self.__growHash()                                                  #Expand the nest array
            resetBitHash = False         
            count = 0        
        
        self.insert(node.key, node.data, resetBitHash, count)                  #Insert evicted
         
            
def __main():
    print("---test duplicates---")
    a  = time.time()
    c = CuckooHash(20)
    for i in range(20):
        c.insert("A", str(i))
    a = time.time() - a
    print("time: " + str(a))
    print(c.find("A") == "0")
    c.delete("A")                                 
    print(c.find("A") == None ) 
    print(c)
    
    print("---test growHash---")
    b = CuckooHash(6)
    b.insert("A", "a")
    b.insert("A", "b")
    b.insert("B", "b")
    b.insert("C", "c") 
    print(b.numOfBuckets()==12) 
    print(b)
    
    
   
    
    


    
if __name__ == '__main__':
    __main()
        
        
        