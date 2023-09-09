# Function for AND operation
def boolean_and(list1, list2):
    return [item for item in list1 if item in list2]

# Function for OR operation
def boolean_or(list1, list2):
    return list(set(list1) | set(list2))

# Function for NOT operation
def boolean_not(list1, universe):
    return [item for item in universe if item not in list1]

# Function to parse and execute Boolean query
def boolean_query_parser(query, inverted_index, doc_ids):
    query_tokens = query.lower().split()
    stack = []
    operator_stack = []

    def apply_operator():
        op = operator_stack.pop()
        if op == "and":
            if len(stack) >= 2:
                list2 = stack.pop()
                list1 = stack.pop()
                stack.append(boolean_and(list1, list2))
            else:
                print("Error: Malformed query. Not enough operands for AND.")
                return []

        elif op == "or":
            if len(stack) >= 2:
                list2 = stack.pop()
                list1 = stack.pop()
                stack.append(boolean_or(list1, list2))
            else:
                print("Error: Malformed query. Not enough operands for OR.")
                return []

        elif op == "not":
            if len(stack) >= 1:
                list1 = stack.pop()
                stack.append(boolean_not(list1, doc_ids))
            else:
                print("Error: Malformed query. Not enough operands for NOT.")
                return []

    for token in query_tokens:
        if token == "and" or token == "or" or token == "not":
            while operator_stack:
                apply_operator()
            operator_stack.append(token)

        elif token == "(":
            operator_stack.append(token)

        elif token == ")":
            while operator_stack and operator_stack[-1] != "(":
                apply_operator()
            if operator_stack:
                operator_stack.pop()  # remove the "("

        else:
            stack.append(inverted_index.get(token, []))

    while operator_stack:
        apply_operator()

    return stack[-1] if stack else []
