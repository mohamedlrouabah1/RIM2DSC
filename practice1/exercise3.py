from collections import deque

def boolean_and(list1, list2) -> list:
    """Function for AND operation"""
    return [item for item in list1 if item in list2]

def boolean_or(list1, list2) -> list:
    """Function for OR operation"""
    return list(set(list1) | set(list2))

def boolean_not(list1, universe) -> list:
    """Function for NOT operation"""
    return [item for item in universe if item not in list1]

def generate_query(sample_queries,list) -> dict:
    """Function to parse and execute Boolean query"""
    query_dictonary = {}
    # enumarate allow me to add ID to a query 
    for query_id, query in enumerate(sample_queries) :
        # init the pile using deque 
        query_tokens = deque(query.lower().split())
        pile = deque()
        op_pile = deque()

        # function operator for AND : OR : NOT
        def operator():
            
            # check if the pile is not empty at start
            if op_pile and pile:
                # get and pop the last element on the pile
                op = op_pile.pop()
                
                # opration AND 
                if op == "and":
                    # check if there is atleast 2 element on the pile
                    if len(pile) >= 2:
                        list2 = pile.pop()
                        list1 = pile.pop()
                        pile.append(boolean_and(list1, list2))
                
                # operation OR
                elif op == "or":
                    # check if there is atleast 2 element on the pile
                    if len(pile) >= 2:
                        list2 = pile.pop()
                        list1 = pile.pop()
                        pile.append(boolean_or(list1, list2))
                
                # operation NOT
                elif op == "not":
                    # check if there is atleast 2 element on the pile
                    if len(pile) >= 1:
                        list1 = pile.pop()
                        pile.append(boolean_not(list1, list[2]))
        while query_tokens:
            # extract and delete the query tokens using pop
            token = query_tokens.popleft()
            
            # if the operator is (AND, OR, NOT), then add to the pile
            if token in ["and", "or", "not"]:
                op_pile.append(token)
            else:  # else occurance to the next
                pile.append(list[0].get(token, []))

        # then apply the remaining operator on the pile since op_pile not empty
        while op_pile:
            operator()

            
        res = pile[0] if pile else []
        query_dictonary[query_id] = res
    # return a dictornary query id + resultat 
    return query_dictonary


def intersect(p1:list, p2:list) -> list:
    """Function to intersect 2 lists"""
    answer = []
    ptr1, ptr2 = 0, 0
    n1, n2 = len(p1), len(p2)
    while p1 != n1 and p2 != n2:
        if p1[ptr1] == p2[ptr2]:
                answer.append(p1[ptr1])
                ptr1 += 1
                ptr2 += 1
        elif p1[ptr1] < p2[ptr2]:
            ptr1 += 1
        else:
            ptr2 += 1
    return answer

if __name__ == "__main__":
    print("module exercice3.py not executable.")