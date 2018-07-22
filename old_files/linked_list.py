class Node():
    def __init__(self):
        self.next_node = None
        self.prev_node = None


class LinkedList():
    def __init__(self, *first_node):
        """
        head is the first node and must be updated consistenly in doubly_link()
        tail is the last node
        the list is initialized with one node either passed to it or generated
        because of this the list length is 1 both ways

        when generating a node
        >>> L = LinkedList()
        >>> type(L)
        <class '__main__.LinkedList'>

        initially they're all the same
        >>> type(L.current_node)
        <class '__main__.Node'>
        >>> L.head is L.tail is L.current_node
        True

        list starts with 1 element
        >>> L.len_list
        1

        list starts at index 0
        >>> L.current_index
        0

        When passing in a node
        >>> N = Node()
        >>> K = LinkedList(N)

        showing they're the same
        >>> K.current_node is N
        True

        same as when generating a node
        K.head is K.tail is K.current_node
        True
        """
        if first_node:
            self.head = first_node[0]
            self.tail = self.head
            self.current_node = self.head
            self.len_list = 1
            self.current_index = 0
        else:
            self.head = self.new_node()
            self.tail = self.head
            self.current_node = self.head
            self.len_list = 1
            self.current_index = 0

    def new_node(self):
        """
        Returns a new node of type Node
        Often used in add_node(new_node()) or append(new_node())
        returns <linked_list.Node object at 0x01010101>
        """ # learn how to handle specific object names with doctest
        NewNode = Node()
        return NewNode

    def add_node(self, NewNode, *index):
        """
        This function takes a node object and an optional index and puts inserts
        the node at the index. If there's no index it insets before current_node

        >>> L = LinkedList()
        >>> L.add_node(L.new_node())
        >>> L.len_list
        2
        """
        if NewNode:
            if index:
                self.go_to(index[0])
                self.doubly_link(NewNode)
            else:
                self.doubly_link(NewNode)
        else:
            raise ValueError("NoneType object provided, requires Node object")

    def doubly_link(self, NewNode):
        """
        When provided a NewNode, this method integrates it into the LinkedList
        instance in the following pattern ([] is the current_node):
        [] prev <-  NewNode
        [] prev ->  NewNode (do these unless current_node has no prev)
                    NewNode <- []
                    NewNode -> []
        With this setup, the NewNode is inserted before current_node

        >>> L = LinkedList()
        >>> L.current_node.name = "Genesis"
        >>> L.doubly_link(L.new_node())
        >>> print(L.current_node.name)
        Genesis
        >>> L.prev_node()
        >>> print(L.current_node.name)
        Traceback (most recent call last):
          ...
        AttributeError: 'Node' object has no attribute 'name'
        """
        try:
            NewNode.prev_node = self.current_node.prev_node
            self.current_node.prev_node.next_node = NewNode
        except (AttributeError):
            self.head = NewNode
        self.current_node.prev_node = NewNode
        NewNode.next_node = self.current_node
        self.len_list+=1
        self.current_index+=1

    def go_to(self, index):
        """
        iterates through the linked list until it reaches your desired index
        If you want to go to 0, it takes you directly rather than looping

        >>> L = LinkedList()
        >>> L.add_node(L.new_node())
        >>> L.current_index
        1
        >>> L.go_to(0)
        >>> L.current_index
        0
        """
        if index is 0:
            self.current_node = self.head
            self.current_index = 0
        else:
            self.desired_index = index
            while self.current_index < self.desired_index:
                try:
                    self.next_node()
                except IndexError:
                    print("Index {} does not exist".format(self.desired_index) )
                    break

            while self.current_index > self.desired_index:
                try:
                    self.prev_node()
                except IndexError:
                    print("Index {} does not exist".format(self.desired_index) )
                    break # TODO: find out if it's ok style to use a break here

    def next_node(self):
        """
        if the next node is not None, then go to next node
        change the current index to reflect that

        >>> L = LinkedList()
        >>> L.add_node(L.new_node())
        >>> L.current_index
        1
        >>> L.next_node()
        Traceback (most recent call last):
            ...
        AttributeError: Current_node does not have a next_node
        >>> L.go_to(0)
        >>> L.current_index
        0
        >>> L.next_node()
        >>> L.current_index
        1
        """
        if self.current_node.next_node:
            self.current_node = self.current_node.next_node
            self.current_index+=1
        else:
            raise AttributeError("Current_node does not have a next_node")

    def prev_node(self):
        """
        if the next node is not None, then go to next node
        change the current index to reflect that
        >>> L = LinkedList()
        >>> L.add_node(L.new_node())
        >>> L.current_index
        1
        >>> L.prev_node()
        >>> L.current_index
        0
        >>> L.prev_node()
        Traceback (most recent call last):
            ...
        AttributeError: Current_node does not have a prev_node

        """
        if self.current_node.prev_node:
            self.current_node = self.current_node.prev_node
            self.current_index-=1
        else:
            raise AttributeError("Current_node does not have a prev_node")

    def append(self, NewNode):
        """
        This function adds a new node to the end of the linked list.
        Note that this leaves current_index at one before the end.
        ^ this is done to prevent unecessary operations

        >>> L = LinkedList()
        >>> L.append(L.new_node())
        >>> L.append(L.new_node())
        >>> L.len_list
        3
        >>> L.current_index
        1
        >>> L.next_node()
        >>> L.next_node()
        Traceback (most recent call last):
          ...
        AttributeError: Current_node does not have a next_node
        >>> L.current_index
        2

        """
        self.go_to(self.len_list-1)
        self.current_node.next_node = NewNode
        NewNode.prev_node = self.current_node
        self.len_list+=1

    def remove(self, *index):
        """
        this function removes the node at current_index
        optionally, it accepts an index to go to before removing it

        >>> L = LinkedList()
        >>> L.append(L.new_node())
        >>> L.append(L.new_node())
        >>> L.current_index
        1
        >>> L.current_node.test_attr = "Keep me!"
        >>> L.go_to(2)
        >>> L.current_node.test_attr = "Remove me!"
        >>> L.remove(2)
        >>> L.len_list
        2
        >>> L.go_to(1)
        >>> L.remove()
        >>> L.len_list
        1
        >>> L.current_node.test_attr
        'Keep me!'

        """
        if self.current_node.next_node or self.current_node.prev_node:
            if index:
                self.go_to(index[0])
            if self.current_node.prev_node and self.current_node.next_node:
                self.current_node.prev_node.next_node = self.current_node.next_node
                self.current_node.next_node.prev_node = self.current_node.prev_node
            elif self.current_node.next_node:
                self.current_node.next_node.prev_node = None
            elif self.current_node.prev_node:
                self.current_node.prev_node.next_node = None
            self.len_list-=1
        else:
            raise Exception("LinkedList must have at least one node")


    def extract_nodes_as_list(self):
        """
        This function returns the nodes of the linked list in a normal list
        >>> L = LinkedList()
        >>> L.add_node(L.new_node())
        >>> alist = []
        >>> alist = L.extract_nodes_as_list()
        >>> for node in alist:
        ...     print(type(node))
        ...
        <class '__main__.Node'>
        <class '__main__.Node'>
        """
        self.go_to(0)
        list_of_nodes = []
        list_of_nodes.append(self.current_node)
        while self.current_node.next_node:
            self.next_node()
            list_of_nodes.append(self.current_node)
        return list_of_nodes

    def print_nodes(self):
        """
        This function prints all the nodes in the list.
        >>> L = LinkedList()
        >>> L.add_node(L.new_node())
        >>> L.add_node(L.new_node())
        >>> L.print_nodes()
        <class '__main__.Node'>
        <class '__main__.Node'>
        <class '__main__.Node'>
        """

        l = self.extract_nodes_as_list()
        for node in l:
            print(type(node))

if __name__=='__main__':
    import doctest
    doctest.testmod()
