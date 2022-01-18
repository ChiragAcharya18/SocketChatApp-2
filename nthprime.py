def isprime(n):
    if n == 4:
        return False
    for i in range(2,n//2):
        if n%i == 0:
            return False
    return True

#n = int(input("Enter the value of n: "))
def nthprime(n):
    i = 2
    m = n
    p = 2
    while(m!=0):
        if isprime(i):
            #primes.append(i)
            p = i
            m = m-1
        i = i+1

    return p
if __name__ == "__main__":
    print(p)
