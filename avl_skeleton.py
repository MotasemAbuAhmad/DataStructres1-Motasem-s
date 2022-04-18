# username - complete info
# id1      - complete info
# name1    - complete info
# id2      - 204327258
# name2    - elhadperl

import random


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type value: str
    @param value: data of your node
    """

    def __init__(self, value, height=0, size=1):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = height

        ### More fields ###
        self.size = size

    """returns the left child
    @rtype: AVLNode
    @returns: the left child of self, None if there is no left child
    """

    def getLeft(self):
        return self.left

    """returns the right child

    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child
    """

    def getRight(self):
        return self.right

    """returns the parent 

    @rtype: AVLNode
    @returns: the parent of self, None if there is no parent
    """

    def getParent(self):
        return self.parent

    """return the value

    @rtype: str
    @returns: the value of self, None if the node is virtual
    """

    def getValue(self):
        return self.value

    """returns the height

    @rtype: int
    @returns: the height of self, -1 if the node is virtual
    """

    def getHeight(self):
        return self.height

    """sets left child

    @type node: AVLNode
    @param node: a node
    """

    def setLeft(self, node):
        self.left = node

    """sets right child

    @type node: AVLNode
    @param node: a node
    """

    def setRight(self, node):
        self.right = node

    """sets parent

    @type node: AVLNode
    @param node: a node
    """

    def setParent(self, node):
        self.parent = node

    """sets value

    @type value: str
    @param value: data
    """

    def setValue(self, value):
        self.value = value

    """sets the balance factor of the node

    @type h: int
    @param h: the height
    """

    def setHeight(self, h):
        self.height = h

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def isRealNode(self):
        if self.height == -1:
            return False
        return True

    def getSize(self):
        return self.size

    def setSize(self, s):
        self.size = s


    def BFcalc(self):
        return (lambda n: n.getLeft().getHeight() - n.getRight().getHeight())(self)

    def hUpdate(self):
        return (lambda n: max(n.getRight().getHeight(), n.getLeft().getHeight()) + 1)(self)

    def sUpdate(self):
        return (lambda n: n.getRight().getSize() + n.getLeft().getSize() + 1)(self)
"""
A class implementing the ADT list, using an AVL tree.
"""


class AVLTreeList(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.root = None
        self.size = 0
        self.first = None
        self.last = None


########### non default constrtr###########
    '''def __init__(self, root : AVLNode):
        self.root = root
        self.size = root.getSize()
        self.first = self.retrieve(0)
        self.last = self.retrieve(root.getSize())'''

    """returns whether the list is empty

    @rtype: bool
    @returns: True if the list is empty, False otherwise
    """

    def empty(self):
        if self.size == 0:
            return True
        return False

    """retrieves the value of the i'th item in the list

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: index in the list
    @rtype: str
    @returns: the the value of the i'th item in the list
    """

    def retrieve(self, i, pr=False):
        return self.retrieve_rec(self.root, i + 1, pr).value

    def retrieve_rec(self, node, i, pr=False):
        """edge cases for testing-                                            ### DELETE AFTER ###"""
        if not isinstance(node, AVLNode):
            print("Error: node is not an AVL Node object")                    ### DELETE AFTER ###"""
        if not node.isRealNode():
            print("Error: node is a VR node")                                  ### DELETE AFTER ###"""

        rank = node.getLeft().size + 1
        if rank == i:
            return node
        if i < rank:
            return self.retrieve_rec(node.getLeft(), i)
        else:
            return self.retrieve_rec(node.getRight(), i - rank)

    """inserts val at position i in the list

    @type i: int
    @pre: 0 <= i <= self.length()
    @param i: The intended index in the list to which we insert val
    @type val: str
    @param val: the value we inserts
    @rtype: list
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def insert(self, i, val):
        counter = 0
        elem = self.initNode(val)             # Initial new node
        if self.empty():                      # Empty list
            self.root = elem
            self.size += 1
            return 0

        if i == self.size:                  # i == len(lst)
            pos = self.appendNode(elem)
        else:
            pos = self.setNode(elem, i)    # Select(self, i+1) == self[i] ==> find the node located in index i
        elem.setParent(pos)
        self.size += 1
        while pos is not None:
            pos.size += 1
            pos.setHeight(pos.hUpdate())
            bf = pos.BFcalc()
            if bf > 1 or bf < -1:
                temp = pos.parent
                counter += 1
                if bf == -2 and pos.getRight().BFcalc() == -1:
                    self.rotateLeft(pos, pos.getRight())
                    counter += 1
                elif bf == -2 and pos.getRight().BFcalc() == 1:
                    self.rotateRight(pos.getRight(), pos.getRight().getLeft())
                    self.rotateLeft(pos, pos.getRight())
                    counter += 2
                elif bf == 2 and pos.getLeft().BFcalc() == 1:
                    self.rotateRight(pos, pos.getLeft())
                    counter += 1
                elif bf == 2 and pos.getLeft().BFcalc() == -1:
                    self.rotateLeft(pos.getLeft(), pos.getLeft().getRight())
                    self.rotateRight(pos, pos.getLeft())
                    counter += 2
                pos = temp

            else:
                pos = pos.parent
        return counter

    def initNode(self, val):
        elem = AVLNode(val)
        vrNodeR = AVLNode(None, -1, 0)
        vrNodeL = AVLNode(None, -1, 0)
        elem.setRight(vrNodeR)
        elem.setLeft(vrNodeL)
        vrNodeR.setParent(elem)
        vrNodeL.setParent(elem)
        return elem

    def appendNode(self, elem):
        pos = self.root
        while pos.getRight().getHeight() != -1:
            pos = pos.right
        pos.setRight(elem)
        return pos

    def setNode(self, elem, i, pr=False):
        pos = self.retrieve_rec(self.root, i + 1, pr)
        if not pos.left.isRealNode():  # if pos.left is vr
            pos.setLeft(elem)
        else:
            pos = pos.left
            while pos.right.getHeight() != -1:
                pos = pos.right
            pos.setRight(elem)
        return pos

    """ t.l  or t.right          
         \             \
          U     -->     R
           \          /   \
            R   -->  U     E   
          /   \       \
         a     E -->   a        """

    def rotateLeft(self, u, r):
        u.setRight(r.getLeft())    # set-> u[right]= a
        u.getRight().setParent(u)  # set-> a[parent]= u
        r.setLeft(u)               # set-> r[left] = u
        r.setParent(u.getParent()) # set-> r[parent]= t
        u.setParent(r)             # set-> u[parent]= r
        if u is self.root:
            self.root = r
        else:
            # if u is not a root, set his parent to r
            if r.getParent().getRight() == u:
                r.getParent().setRight(r)
            else:
                r.getParent().setLeft(r)
        # Fix size & height
        u.setSize(u.sUpdate())
        u.setHeight(u.hUpdate())
        r.setSize(r.sUpdate())
        r.setHeight(r.hUpdate())
        #print(u.height, r.height)

    def rotateRight(self, u, l):
        u.setLeft(l.getRight())
        u.getLeft().setParent(u)
        l.setRight(u)
        l.setParent(u.getParent())
        u.setParent(l)
        if u is self.root:
            self.root = l
        else:
            if l.getParent().getLeft() == u:
                l.getParent().setLeft(l)
            else:
                l.getParent().setRight(l)
        """print([["u.left.height: "+str(u.getLeft().getHeight())],["u.height: "+str(max(u.getLeft().getHeight(),u.getRight().getHeight())+1)],
               ["u.right.height: "+str(u.getRight().getHeight())]])"""
        u.setSize(u.sUpdate())
        u.setHeight(u.hUpdate())
        l.setSize(l.sUpdate())
        """print([["l.left.height: " + str(l.getLeft().getHeight())],
               ["l.height: " + str(max(l.getLeft().getHeight() , l.getRight().getHeight()) + 1)],
               ["l.right.height: " + str(l.getRight().getHeight())]])"""
        l.setHeight(l.hUpdate())


    def fixUp(self, pos, insert=True):
        counter = 0
        while pos is not None:
            pos.size += (lambda act: 1 if insert else -1)(insert)
            pos.setHeight(pos.hUpdate())
            bf = pos.BFcalc()
            if bf > 1 or bf < -1:
                temp = pos.parent
                if bf == -2 and (lambda bfc: pos.getRight().BFcalc() == -1 if insert else
                        (pos.getRight().BFcalc() == -1 or pos.getRight().BFcalc() == 0))(insert):
                    self.rotateLeft(pos, pos.getRight())
                    counter += 1
                elif bf == -2 and pos.getRight().BFcalc() == 1:
                    self.rotateRight(pos.getRight(), pos.getRight().getLeft())
                    self.rotateLeft(pos, pos.getRight())
                    counter += 2
                elif bf == 2 and (lambda bfc: pos.getLeft().BFcalc() == 1 if insert else
                        (pos.getLeft().BFcalc() == 1 or pos.getLeft().BFcalc() == 0))(insert):
                    self.rotateRight(pos, pos.getLeft())
                    counter += 1
                elif bf == 2 and pos.getLeft().BFcalc() == -1:
                    self.rotateLeft(pos.getLeft(), pos.getLeft().getRight())
                    self.rotateRight(pos, pos.getLeft())
                    counter += 2
                pos = temp

            else:
                pos = pos.parent
        if not insert and self.getSize() == 0:
            self.root = None
        return counter

    """deletes the i'th item in the list
    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list to be deleted
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, i):
        counter = 0
        self.size -= 1
        dNode = self.retrieve_rec(self.root, i + 1)
        # case 1- dNode is a leaf
        if not (dNode.getRight().isRealNode() or dNode.getLeft().isRealNode()):
            pos = self.deleteLeaf(dNode)

        # case 2- dNode has two children
        elif dNode.getRight().isRealNode() and dNode.getLeft().isRealNode():
            sNode = self.findSuccessorD(dNode)  # Find dNode's successor

            if not sNode.getRight().isRealNode() and not sNode.getLeft().isRealNode():
                pos = self.deleteLeaf(sNode)  # case 2.a- sNode is a leaf

            else:  # case 3.b- sNode is a branch
                pos = self.deleteXor(sNode)
            if pos is dNode:  # Edge case- Successor(dNode) == sNode
                pos = sNode
            self.exchangeNodes(dNode, sNode)  # set sNode in dNode location

        else:  # XOR(right(isReal(), left(isReal))
            pos = self.deleteXor(dNode)
        #counter = self.fixUp(pos, False)
        # Fixing up to root
        while pos is not None:
            pos.size -= 1
            pos.setHeight(pos.hUpdate())
            bf = pos.BFcalc()
            if bf > 1 or bf < -1:
                temp = pos.parent
                if bf == -2 and (pos.getRight().BFcalc() == -1 or pos.getRight().BFcalc() == 0):
                    self.rotateLeft(pos, pos.getRight())
                    counter += 1
                elif bf == -2 and pos.getRight().BFcalc() == 1:
                    self.rotateRight(pos.getRight(), pos.getRight().getLeft())
                    self.rotateLeft(pos, pos.getRight())
                    counter += 2
                elif bf == 2 and (pos.getLeft().BFcalc() == 1 or pos.getLeft().BFcalc() == 0):
                    self.rotateRight(pos, pos.getLeft())
                    counter += 1
                elif bf == 2 and pos.getLeft().BFcalc() == -1:
                    self.rotateLeft(pos.getLeft(), pos.getLeft().getRight())
                    self.rotateRight(pos, pos.getLeft())
                    counter += 2
                pos = temp
            else:
                pos = pos.parent
        if self.size == 0:
            self.root = None
        return counter

    def deleteLeaf(self, dNode):
        dnp = dNode.getParent()
        if dNode is not self.root:
            if dnp.getRight() is dNode:
                dnp.setRight(dNode.getRight())
                dNode.getRight().setParent(dnp)
            else:
                dnp.setLeft(dNode.getLeft())
                dNode.getLeft().setParent(dnp)
        else:
            self.root = None
        return dnp

    def deleteXor(self, dNode):
        dnp = dNode.getParent()
        if dNode.getRight().isRealNode():
            dNode.getRight().setParent(dnp)
            if dNode is self.root:
                self.root = dNode.getLeft()
                return dnp

            if dnp.getRight() is dNode:
                dnp.setRight(dNode.getRight())
            else:
                dnp.setLeft(dNode.getRight())
        else:
            dNode.getLeft().setParent(dnp)
            if dNode is self.root:
                self.root = dNode.getRight()
                return dnp
            if dnp.getRight() is dNode:
                dnp.setRight(dNode.getLeft())
            else:
                dnp.setLeft(dNode.getLeft())
        return dnp

    def exchangeNodes(self, dNode, sNode):
        dnp = dNode.getParent()
        sNode.setParent(dNode.getParent())  # 6.p =none
        sNode.setLeft(dNode.getLeft())
        dNode.getLeft().setParent(sNode)
        if dNode.getRight() is not sNode:
            sNode.setRight(dNode.getRight())
            dNode.getRight().setParent(sNode)
        sNode.setSize(dNode.size)
        if dNode is not self.root:
            if dnp.getRight() is dNode:
                dnp.setRight(sNode)
            else:
                dnp.setLeft(sNode)
        else:
            self.root = sNode

    """
    dNode.setRight(None)
    dNode.setLeft(None)
    dNode.setLeft(None)
    """

    def findSuccessorD(self, pos):
        pos = pos.getRight()
        while pos.getLeft().isRealNode():
            pos = pos.getLeft()
        return pos

    """returns the value of the first item in the list
    @rtype: str
    @returns: the value of the first item, None if the list is empty
    """

    def first(self):
        return (self.retrieve(0)).getValue()

    """returns the value of the last item in the list

    @rtype: str
    @returns: the value of the last item, None if the list is empty
    """

    def last(self):
        return (self.retrieve(self.length() - 1)).getValue()

    """returns an array representing list 

    @rtype: list
    @returns: a list of strings representing the data structure
    """

    def listToArray(self):
        return res

    """returns the size of the list 

    @rtype: int
    @returns: the size of the list
    """

    def length(self):
        return self.size


    def setRoot(self, root:AVLNode):
        self.root = root
        if root != None:
            self.size = root.getSize()

    def setSize(self, n):
        self.size = n
    """splits the list at the i'th index

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list according to whom we split
    @rtype: list
    @returns: a list [left, val, right], where left is an AVLTreeList representing the list until index i-1,
    right is an AVLTreeList representing the list from index i+1, and val is the value at the i'th index.
    """
    def createTreefromNode(self, node : AVLNode):
        Tree = AVLTreeList()
        node.setParent(None)
        Tree.setRoot(node)
        Tree.setSize(node.getSize())
        return Tree

    def split(self, i):
        res = []
        node = self.retNode(self.getRoot(), i)
        leftT = self.createTreefromNode(node.getLeft())
        rightT = self.createTreefromNode(node.getRight())
        val = node.getValue()
        parent = node.getParent()
        while parent != None:
            leftT.printTree("current left")
            rightT.printTree("current Right")
            if parent.getRight() == node:
                node = parent
                parent = node.getParent()
                leftSubTree = self.createTreefromNode(node.getLeft())
                leftT = self.join(leftSubTree, node, leftT)
            else:
                node = parent
                parent = node.getParent()
                rightSubTree = self.createTreefromNode(node.getRight())
                rightT = self.join(rightT, node, rightSubTree)

        res.append(leftT)
        res.append(val)
        res.append(rightT)
        return res

    def retNode(self, r, i):
        smaller = (r.getLeft()).getSize()
        if smaller < i:
            return self.retNode(r.getRight(), i - smaller - 1)
        elif smaller > i:
            return self.retNode(r.getLeft(), i)
        else:
            return r

    """concatenates lst to self

    @type lst: AVLTreeList
    @param lst: a list to be concatenated after self
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    """

    def concat(self, lst):
        height_l = self.getRoot().getHeight()
        height_r = lst.getRoot().getHeight()
        x = self.getRightMost(self.getRoot())
        self.delete(self.length() - 1)
        x.setParent(None)
        joinedTrees = self.join(self, x, lst)
        self.setRoot(joinedTrees.getRoot())
        self.setSize(joinedTrees.getSize())
        return abs(height_l - height_r)

    def getRightMost(self, node):
        while node.getRight().isRealNode():
            node = node.getRight()
        return node

    def getLeftMost(self, node):
        while node.getLeft().isRealNode():
            node = node.getLeft()
        return node


    def join(self, lst1, x: AVLNode, lst2):
        lst1.printTree("first tree")
        lst2.printTree("second tree")
        if lst1.empty() and lst2.empty():
            lst2.insert(lst2.getSize(), x.getValue())
            return lst2
        if lst1.empty():
            lst2.insert(0 , x.getValue())
            return lst2
        if lst2.empty():
            lst1.insert(lst1.getSize() , x.getValue())
            return lst1

        lst1Height = lst1.getRoot().getHeight()
        lst2Height = lst2.getRoot().getHeight()
        diff = abs(lst1Height-lst2Height)

        if lst1Height == lst2Height or diff == 1:#no need to rebalance
            x.setLeft(lst1.getRoot())
            x.setRight(lst2.getRoot())
            self.nodeHandSupdate(x)
            newT = self.createTreefromNode(x)
            return newT

        if lst1Height < lst2Height:
            b = self.reachHeightLeft(lst2, lst1Height)
            x.setLeft(lst1.getRoot())
            x.setRight(b)
            self.nodeHandSupdate(x)
            c = b.getParent()
            c.setLeft(x)
            self.nodeHandSupdate(c)
            self.fixUp(c, False)
        else:
            b = self.reachHeightRight(lst1, lst2Height)
            x.setLeft(b)
            x.setRight(lst2.getRoot())
            self.nodeHandSupdate(x)
            c = b.getParent()
            c.setRight(x)
            self.nodeHandSupdate(c)
            self.fixUp(c, False)
        if lst1Height < lst2Height:
            return lst2
        else:
            return lst1

    def nodeHandSupdate(self, node:AVLNode):
        node.setSize(node.getLeft().getSize() + node.getRight().getSize() + 1)
        node.setHeight(max(node.getLeft().getHeight(), node.getRight().getHeight()) + 1)
    def reachHeightLeft(self, tree, h):
        node = tree.getRoot()
        while node.getHeight() > h:
            node = node.getLeft()
        return node
    def reachHeightRight(self, tree, h):
        node = tree.getRoot()
        while node.getHeight() > h:
            node = node.getRight()
        return node

    """searches for a *value* in the list

    @type val: str
    @param val: a value to be searched
    @rtype: int
    @returns: the first index that contains val, -1 if not found.
    """

    def search(self, val):
        node = self.root
        return self.search_rec(self, node, val)

    def search_rec(self, node, val):
        if node.getValue() == val:
            return -1 #maybe 0??
        smaller = node.getLeft().size()
        if node.getValue() < val:
            return node.getLeft().getSize() + self.search_rec(node.getRight(), val)
        else:
            return self.search_rec(node.getLeft(), val)


    """returns the root of the tree representing the list

    @rtype: AVLNode
    @returns: the root, None if the list is empty
    """

    def getRoot(self):
        if self.empty():
            return None
        return self.root

    # More functions
    def getSize(self):
        return self.size

    def select(self, i):
        return self.retrieve_rec(self.root, i + 1)

    def rank(self, val):
        return self.search(val)

    ######################################## Put these functions ########################################
    ##################################### inside AVLTreeList class ######################################

    """Checks if the AVL tree properties are consistent

    @rtype: boolean 
    @returns: True if the AVL tree properties are consistent
    """



    def check(self, name):
        pt = True
        if not self.isAVL():
            print("The tree is not an AVL tree!")
            pt = False
        if not self.isSizeConsistent():
            print("The sizes of the tree nodes are inconsistent!")
            pt = False
        if not self.isHeightConsistent():
            print("The heights of the tree nodes are inconsistent!")
            pt = False

        return pt


    # if not self.isRankConsistent():
    # print("The ranks of the tree nodes are inconsistent!")

    """Checks if the tree is an AVL

    @rtype: boolean 
    @returns: True if the tree is an AVL tree
    """

    def isAVL(self):
        if self.root is None and self.size !=0:
            print("XXX :ERROR: isAVL() --> self.root is None and self.size !=0")
        if self.size == 0:
            return True
        return self.isAVLRec(self.getRoot())

    """Checks if the subtree is an AVL
    @type x: AVLNode
    @param x: The root of the subtree
    @rtype: boolean 
    @returns: True if the subtree is an AVL tree
    """

    def isAVLRec(self, x):
        # If x is a virtual node return True
        if not x.isRealNode():
            return True
        # Check abs(balance factor) <= 1
        bf = (lambda n: n.getLeft().getHeight() - n.getRight().getHeight())(x)
        if bf > 1 or bf < -1:
            print("Criminal BF -----> XXXXXXXXX  "+x.getValue()+"  XXXXXXXXXX")
            return False
        # Recursive calls
        return self.isAVLRec(x.getLeft()) and self.isAVLRec(x.getRight())

    """Checks if sizes of the nodes in the tree are consistent

    @rtype: boolean 
    @returns: True if sizes of the nodes in the tree are consistent
    """

    def isSizeConsistent(self):
        if self.size == 0:
            return True
        return self.isSizeConsistentRec(self.getRoot())

    """Checks if sizes of the nodes in the subtree are consistent

    @type x: AVLNode
    @param x: The root of the subtree
    @rtype: boolean 
    @returns: True if sizes of the nodes in the subtree are consistent
    """

    def isSizeConsistentRec(self, x):
        # If x is a virtual node return True
        if not x.isRealNode():
            if x.size == 0:
                return True
            else:
                return False
        # Size of x should be x.left.size + x.right.size + 1
        if x.size != (x.getLeft().size + x.getRight().size + 1):
            print("Criminal Size -----> XXX"+str(x.size)+"XXXX  " + x.getValue() + "  XXXX"+str(x.size)+"XXXXXX")
            return False
        # Recursive calls
        return self.isSizeConsistentRec(x.getLeft()) and self.isSizeConsistentRec(x.getRight())

    """Checks if heights of the nodes in the tree are consistent

    @rtype: boolean 
    @returns: True if heights of the nodes in the tree are consistent
    """

    def isHeightConsistent(self):
        if self.size == 0:
            return True
        return self.isHeightConsistentRec(self.getRoot())

    """Checks if heights of the nodes in the subtree are consistent

    @type x: AVLNode
    @param x: The root of the subtree
    @rtype: boolean 
    @returns: True if heights of the nodes in the subtree are consistent
    """

    def isHeightConsistentRec(self, x):
        # If x is a virtual node return True
        if not x.isRealNode():
            return True
        # Height of x should be maximum of children heights + 1
        if x.getHeight() != max(x.getLeft().getHeight(), x.getRight().getHeight()) + 1:
            print("Criminal Height -----> XXX ["+str(x.height)+" ]XXXX  " + x.getValue() + "  XXXX[ "+str(x.height)+"] XXXXXX")
            return False
        # Recursive calls
        return self.isSizeConsistentRec(x.getLeft()) and self.isSizeConsistentRec(x.getRight())

    """Checks if the ranks of the nodes in the tree are consistent

    @returns: True if the ranks of the nodes in the tree are consistent
    """

    def isRankConsistent(self):
        root = self.getRoot()
        for i in range(1, root.size):
            if i != self.rank(self.retrieve_rec(i + 1)):
                return False
        """nodesList = self.nodes()
        for node in nodesList:
        if node != self.retrieve_rec(self.search(node)):
        return False"""
        return True

    """Returns a list of the nodes in the tree sorted by index in O(n)

    @rtype: list
    @returns: A list of the nodes in the tree sorted by index
    """

    def nodes(self):
        lst = []
        self.nodesInOrder(self.getRoot(), lst)
        return lst

    """Adds the nodes in the subtree to the list
     following an in-order traversal in O(n)

    @type x: AVLNode
    @type lst: list
    @param x: The root of the subtree
    @param lst: The list
    """

    def nodesInOrder(self, x, lst, pr=False):
        if not x.isRealNode():
            return
        self.nodesInOrder(x.getLeft(), lst)
        lst.append(x)
        self.nodesInOrder(x.getRight(), lst)

    def oneRandomInsert(self, lst, th, strings=True):
        if not self.check("Before insert: "+str(th)):
            print("Given tree is not correct")
            return False
        treeB = printree(self)
        index = random.randint(0, self.getSize())
        if strings:
            type = random.randint(1, 2)
        else:
            type = 1
        if type == 2:
            lengthStr = random.randint(2, 7)
            val = strGenerator(lengthStr)
        else:
            val = str(random.randint(0, 100))
        self.insert(index, val)
        if not self.check("Before insert: "+str(th)):
            print("before")
            for j in treeB:
                print(j)
            print("Tree after insert val # [" + val + "] # is not correct")
            self.printTree("After")
            return False
        return True

    def check1_i_d(self, l1):
        for i in range(len(l1)):
            #print("### TEST " + chr(i + 65) + " ###\n", l1)
            # t1.printTree("Del " + chr(i + 65) + "[size=" + str(t1.size) + "]")
            # arrayPrinter(t1)
            val = self.retrieve(i)
            #print("\n", chr(i + 65) + ".) Delete value #", val, "#")
            self.delete(i)
            del l1[i]
            # print("After delete(", val, "):\n", l1)
            #self.check("After delete(" + val + "):\n")
            #self.printTree("AFTER DEL [" + chr(i + 65) + "]")
            # arrayPrinter(t1)
            s = True
            for j in range(9):
                if self.retrieve(j) != l1[j]:
                    s = False
                    #print("failed -> t1.retrieve(", j, ") != l1[", j, "] --> ", t1.retrieve(j), " != ", l1[j], "", )
            self.insert(i, val)
            l1.insert(i, val)
            if s:
                print("\n$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print("$$$$$$$$   ", chr(i + 65) + " IS A SUCCESS TEST !!!   $$$$$$$$")
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print("\n")
        #self.printTree("Initial tree")
        #print(l1)

    def testInsert1(self, lst, name):
        pos = self.check("Para check")
        if not pos:
            ls = self.nodes()
            return False
        self.insert()




    """ Check if avl tree is handle random insert actions
        :param [ tree, lst, name, limit of insertions]
        """

    def checkInsert(self, lst, name, limit=15):
        passTest = True
        print("Check insert test (input=#", name, "#):   *(50 inserts)")
        if self.size != len(lst):
            passTest = False
            print("Size of given tree #", name, "# != len(lst) --> ", self.size, "!=", len(lst))
        testAvl = self.check(name)
        if not testAvl:
            print("The criminal is ---->  XXXXXXX  " + val + "  XXXXXXX")
            self.printTree("with criminal " + val + " (size= " + str(self.getSize()) + ")")
        for i in range(limit):
            index = random.randint(0, self.getSize())
            val = str(random.randint(65, 122))
            self.insert(index, val)
            lst.insert(index, val)
            if self.size != len(lst):
                passTest = False
                print("Iter num. ", i + 1, ": Size of the tree #", name + " insert("+str(i)+")", "# != len(lst) --> ", self.size, "!=",
                      len(lst))
            testAvl = self.check(name)
            if not testAvl:
                print("The criminal is ---->  XXXXXXX  " +val + "  XXXXXXX")
                self.printTree("insert("+str(i)+") with criminal "+val+" (size= "+str(self.getSize())+")")
        for i in range(self.size):
            if self.retrieve(i) != lst[i]:
                passTest = False
                print("AVLtree[", i, "] != lst[", i, "] --> # ", self.retrieve(i), " != ", lst[i])
        if passTest:
            print("Good! AVL tree #", name, "# passed the test")
        return passTest




    def checkDelete(self, lst, name):
        passTest = True
        print("Check insert test (input=#", name, "#):   *(50 inserts)")
        if self.size != len(lst):
            passTest = False
            print("Size of the tree #", name, "# != len(lst) --> ", self.size, "!=", len(lst))
        delNum = random.randint(1, self.getSize())
        for i in range(delNum):
            index = random.randint(0, self.getSize() - 1)
            avlElem = self.retrieve()
            lstElem = lst[index]
            self.delete(index)
            del lst[index]
            # CHECK IF LST==AVL
            for j in range(self.getSize()):
                rIndex = random.randint(0, self.getSize() - 1)
                if self.retrieve(rIndex) != lst[rIndex]:
                    passTest = False
                    print("AVLtree[", rIndex, "] != lst[", rIndex, "] --> # ", self.retrieve(rIndex), " != ",
                          lst[rIndex])
                    print("Criminal deletion --> AVL[", index, "]:", avlElem, "|| lst[", index, "]:", lstElem)

        if passTest:
            print("###########################\nGood! AVL tree #", name, "# passed the test\n###################################")

    def printTree(self, name=""):
        print("AVL tree: ", name)
        tLst = printree(self)
        for n in tLst:
            print(n)

    def lstDetails(self):
        nodesLst = self.nodes()
        lstV = [nodesLst[j].value for j in range(len(nodesLst))]
        lstS = [nodesLst[j].getSize() for j in range(len(nodesLst))]
        lstH = [nodesLst[j].getHeight() for j in range(len(nodesLst))]
        lstB = [nodesLst[j].BFcalc() for j in range(len(nodesLst))]
        laN = lambda x: "None!" if x is None else x.getValue()
        # laN2 =
        lstD = [[laN(nodesLst[j].getLeft()), laN(nodesLst[j].getParent()), laN(nodesLst[j].getRight())] for j in
                range(len(nodesLst))]
        print(lstV)
        print(lstS)
        print(lstH)
        print(lstB)
        print(lstD)

    """ Lists generator
    :rType: (AVL tree , Array) 
    :return: AVL tree list , Array list
    """


def listsGenerator(limit):
    t = AVLTreeList()
    lst = []
    chooseLen = random.randint(0, limit)
    for i in range(chooseLen):
        chooseType = random.randint(1, 3)  # 3-> string , 2 -> int, 1 -> char
        if chooseType == 3:
            lengthStr = random.randint(2, 7)
            val = strGenerator(lengthStr)
        elif chooseType == 2:
            val = str(random.randint(0, 100))
        else:
            val = chr(random.randint(97, 122))
        index = random.randint(0, i)
        t.insert(index, val)
        lst.insert(index, val)
        t.check("random generator")

    return t, lst


def strGenerator(len):
    res = [chr(random.randint(65, 90)) for i in range(len)]
    return "".join(res)


def arrayPrinter(t):
    lt = t.nodes()
    lb = []
    lv = []
    for k in range(len(lt)):
        e = []
        d = []
        if not isinstance(lt[k], AVLNode):
            print("None node in lt[", k, "] -> should be a vr!")
            lv.append("None")
            d.append("None -->")
        else:
            if lt[k].value is None:
                lv.append("VR")
                d.append("VR -->")
            else:
                lv.append(lt[k].value)
                d.append(lt[k].value + " -->")

        if not isinstance(lt[k].left, AVLNode):
            print("None node in lt[", k, "].Left -> should be a vr!")
            e.append("N")
        else:
            if lt[k].left is None:
                e.append("VR")
            else:
                e.append(lt[k].left.value)

        if not isinstance(lt[k].parent, AVLNode) and lt[k] is not t.root:
            print("None node in lt[", k, "].parent -> not root, so it is a mistake")
        else:
            if lt[k].parent is None:
                e.append("None of root")
            else:
                e.append(lt[k].parent.value)

        if not isinstance(lt[k].right, AVLNode):
            print("None node in lt[", k, "].Right -> should be a vr!")
        else:
            if lt[k].right is None:
                e.append("VR")
            else:
                e.append(lt[k].right.value)
        d.append(e)
        lb.append(d)
    if len(lt) != len(lb):
        print("sizes not good")
    print("\nList of values in order: ", lv)
    print("List of branches in order: ", lb, "\n")


def main():
    t1, t2, t3 = AVLTreeList(), AVLTreeList(), AVLTreeList()
    l1 = [str(i) for i in range(100)]  # [0, 1, 2, 3, ... , 9]
    l2 = [str(i) for i in range(0, 300, 2)]  # [0, 2, 4, 6, ... , 18]
    l3 = [chr(i) for i in range(65, 91)]  # ['a', 'b', 'c', ... , 'z']
    i1 = [t1.insert(i, str(i)) for i in range(100)]  # [0, 1, 2, 3, ... , 9]
    i2 = [t2.insert(i / 2, str(i)) for i in range(0, 300, 2)]  # [0, 2, 4, 6, ... , 18]
    i3 = [t3.insert(i - 65, chr(i)) for i in range(65, 91)]  # ['a', 'b', 'c', ... , 'z']"""
    ##########Motasem#################
    t1.printTree("self list")
    t3.printTree("other list")
    xx = t1.concat(t3)
    t1.printTree("after concat")
    t1.check("t1 tree")
    '''lst = t1.split(31)
    lst[0].printTree("left part")
    print("the value of 100th element is", lst[1])
    lst[2].printTree("right part")
    lst[0].check("left  part")
    lst[2].check("right part")'''
   # printree(lst[2])
    '''t1.check1_i_d(l1)
    mistakesLst =[]
    for i in range(1):
        t, l = listsGenerator(23)
        if not t.checkInsert(l, "test "+str(i)):
            mistakesLst.append([t,l])
    t4 = AVLTreeList()
    t4.insert(0,"114")
    t4.insert(1,"118")
    t4.insert(1,"107")
    t4.printTree("last")
    print(t4.root.size)
    l2 = []
    for i in range(500):
        test = t2.oneRandomInsert(l2,i)
        #t2.printTree()

        if not test:
            print("Falseeeeeeeeeeeeeeeeeeeeeeee")
            nodesLst = t2.nodes()
            lstV = [nodesLst[j].value for j in range(len(nodesLst))]
            lstS = [nodesLst[j].getSize() for j in range(len(nodesLst))]
            lstH = [nodesLst[j].getHeight() for j in range(len(nodesLst))]
            lstB = [nodesLst[j].BFcalc() for j in range(len(nodesLst))]
            laN = lambda x: "None!" if x is None else x.getValue()
            #laN2 =
            lstD = [[laN(nodesLst[j].getLeft()), laN(nodesLst[j].getParent()), laN(nodesLst[j].getRight()) ] for j in range(len(nodesLst))]
            print(lstV)
            print(lstS)
            print(lstH)
            print(lstB)
            print(lstD)
            break'''





#################################################################################################
#################################################################################################

                                  ### PRINTER FUNCTION ###
def printree(t, bykey=False):
    """Print a textual representation of t
    bykey=True: show keys instead of values"""
    return trepr(t, t.getRoot(), bykey)


def trepr(t, node, bykey=False):
    """Return a list of textual representations of the levels in t
    bykey=True: show keys instead of values"""
    if not isinstance(node, AVLNode):
        return ["None"]

    if not node.isRealNode():  # You might want to change this, depending on your implementation
        return ["#"]  # Hashtag marks a virtual node

    thistr = str(node.getValue())

    return conc(trepr(t, node.getLeft(), bykey), thistr, trepr(t, node.getRight(), bykey))


def conc(left, root, right):
    """Return a concatenation of textual representations of
    a root node, its left node, and its right node
    root is a string, and left and right are lists of strings"""

    lwid = len(left[-1])
    rwid = len(right[-1])
    rootwid = len(root)

    result = [(lwid + 1) * " " + root + (rwid + 1) * " "]

    ls = leftspace(left[0])
    rs = rightspace(right[0])
    result.append(ls * " " + (lwid - ls) * "_" + "/" + rootwid * " " + "\\" + rs * "_" + (rwid - rs) * " ")

    for i in range(max(len(left), len(right))):
        row = ""
        if i < len(left):
            row += left[i]
        else:
            row += lwid * " "

        row += (rootwid + 2) * " "

        if i < len(right):
            row += right[i]
        else:
            row += rwid * " "

        result.append(row)

    return result


def leftspace(row):
    """helper for conc"""
    # row is the first row of a left node
    # returns the index of where the second whitespace starts
    i = len(row) - 1
    while row[i] == " ":
        i -= 1
    return i + 1


def rightspace(row):
    """helper for conc"""
    # row is the first row of a right node
    # returns the index of where the first whitespace ends
    i = 0
    while row[i] == " ":
        i += 1
    return i


if __name__ == "__main__":
    main()
