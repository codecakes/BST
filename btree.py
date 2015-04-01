"""Implement a Binary Search Tree

A binary tree would be an object.
A Tree object will be a collection of nodes.

You can:
    
    - Insert nodes
    - Delete nodes
    - Merge Trees - merge by using Insert nodes.
    - Rebalance Trees
"""

from math import floor, log
from operator import add
from collections import deque


class bnode(object):
    """Node level operations"""
    
    def __init__(self, root_node, value=None, left_node = None, right_node = None, parent_node = None):
        
        self.height = 0  #height of this node in a tree
        self.reverse_height = 0  #height from leaf to current node
        
        if isinstance(root_node ,(int, float, long)):
            self.root_node = root_node
        else:
            raise Exception("root node type is not a numeric. it can only be a numeric")
        self.val = value
        #add left and right nodes as bnode class
        self.add_left(left_node)
        self.add_right(right_node)
        self.add_parent(parent_node)
    
    def level(self, n):
        """return level of tree given number of nodes"""
        return floor(log(n, 2))
    
    def set_node_val(self, value):
        self.val = value    
    
    def add_left(self, left_node):
        """Add to left node and point left child to the current calling node"""
        if isinstance(left_node, bnode) and left_node.root_node <= self.root_node:
            self.left_node = left_node
            self.left_node.add_parent(self)
    
    def add_right(self, right_node):
        """Add to right node and point right child to the current calling node"""
        if isinstance(right_node, bnode) and right_node.root_node > self.root_node:
            self.right_node = right_node
            self.right_node.add_parent(self)
    
    def add_parent(self, parent_node):
        """
        Point current Node to a Parent Node.
        Add current height as Parent height + 1.
        """
        if isinstance(parent_node, bnode):
            self.parent_node = parent_node
            self.height = self.parent_node.height + 1
    
    def hasParent(self):
        """Whether this node has a parent node"""
        return True if hasattr(self, 'parent_node') else False
    
    def hasRightChild(self):
        """Whether this node has a right child node"""
        return True if hasattr(self, 'right_node') else False
    
    def hasLeftChild(self):
        """Whether this node has a left child node"""
        return True if hasattr(self, 'left_node') else False
    
    def isParent(self, node):
        """Whether this node is a parent node to a given bnode object, node"""
        return node.parent_node == self if node.hasParent() else False
    
    def isRightChild(self):
        """Whether this node is a right child node to a parent"""
        if self.hasParent():
            if self.parent_node.hasRightChild():
                return self.parent_node.right_node == self
        return False
    
    def isLeftChild(self):
        """Whether this node is a left child node to a parent"""
        if self.hasParent():
            if self.parent_node.hasLeftChild():
                return self.parent_node.left_node == self
        return False
    
    def isLeaf(self):
        """
        return False If it has no left or right child, then it is a leaf 
        else return True
        """
        return not (self.hasLeftChild() or self.hasRightChild())
    
    def add_child_node(self, node):
        """Add a child node to left or right child position whichever is legit.
        #recursive approach
        if isinstance(node, bnode):
            if node.root_node < self.root_node:
                if self.hasLeftChild():
                    #if left child node already exists
                    self.left_node.add_child_node(node)
                else:
                    #add to left node
                    self.add_left(node)
            elif node.root_node > self.root_node:
                if self.hasRightChild():
                    #if right child node already exists
                    self.right_node.add_child_node(node)
                else:
                    #add to right node
                    self.add_right(node)
            else:
                #Raise exception for duplicate keys
                print node.root_node
                raise Exception("Node with this key already exists")
        log(N) operation.
        """
        # a non recur solution
        done = 0
        target_node = self
        if isinstance(node, bnode):
            while not done:
                if node.root_node < target_node.root_node:
                    if target_node.hasLeftChild():
                        #if left child node already exists
                        target_node = target_node.left_node
                    else:
                        #add to left node
                        target_node.add_left(node)
                        done = 1
                elif node.root_node > target_node.root_node:
                    if target_node.hasRightChild():
                        #if right child node already exists
                        target_node = target_node.right_node
                    else:
                        #add to right node
                        target_node.add_right(node)
                        done = 1
                elif node.root_node == target_node.root_node:
                    #Raise exception for duplicate keys
                    print node.root_node
                    raise Exception("Node with this key already exists")
            return
    
    def remove(self, node):
        """
        Removes the node from the Calling Parent Node.
        And Removes the caller Parent from the node itself.
        """
        if node.hasParent() and self.isParent(node):
            if node.isLeftChild() and node.parent_node.left_node == node:
                delattr(self, 'left_node')
            elif node.isRightChild() and node.parent_node.right_node == node:
                delattr(self, 'right_node')
            print "DELETING PARENT NODE ASSOCIATION"
            delattr(node, 'parent_node')
        
    
    def refreshHeight(self):
        """eval and get maximum height from current node to bottom leaf"""
        node = self
        temp = deque([node])
        
        while temp:
            target_node = temp.popleft()
            if not target_node.hasParent():
                target_node.height = 0
            else:
                target_node.height = target_node.parent_node.height + 1
            if target_node.hasLeftChild():
                temp.append(target_node.left_node)
            if target_node.hasRightChild():
                temp.append(target_node.right_node)
        return
    
    def getMaxHeight(self):
        """get maximum height/depth till leaf nodes treating current node as root"""
        max_height = 0
        temp = deque([self])
        
        while temp:
            target_node = temp.popleft()
            
            if not target_node.isLeaf():
                if target_node.hasLeftChild():
                    temp.append(target_node.left_node)
                if target_node.hasRightChild():
                    temp.append(target_node.right_node)
            if target_node.height > max_height:
                max_height = target_node.height
        return max_height
    
    def revHeight(self):
        """
        Evaluate and get maximum height from bottom leaf to current node.
        
        #recursive way:
        left = right = 0
        if not self.isLeaf():
            if self.hasLeftChild():
                left = self.left_node.revHeight() + 1
            if self.hasRightChild():
                right = self.right_node.revHeight() + 1
            self.reverse_height = max(left, right)
        else:
            self.reverse_height = 0
        del left, right
        return self.reverse_height
        """
        #tot_nodes: Number of nodes as input to calculate levels in the tree.
        tot_nodes = self.find_tot_nodes()
        #store operation
        def store_op(tot_nodes):
            level = 0
            max_level = self.level(tot_nodes)  #max levels at given total nodes
            store_list = deque()
            store_list.appendleft([self])
            
            while level <= max_level and max_level > 0:
                l = store_list[0]
                temp = []
                for node in l:
                    if not node.isLeaf():
                        if node.hasLeftChild():
                            temp.append(node.left_node)
                        if node.hasRightChild():
                            temp.append(node.right_node)
                    else:
                        node.reverse_height = 0
                        temp.append(node)
                store_list.appendleft(temp)
                level += 1
            return store_list
        
        def evaluate(store_list):
            """
            Evaluate reverse height 
            given a list of nodes leaves to root node L-R.
            root node is the current calling node
            and may not necessarily be the actual root of the tree.
            """
            #In each list of nodes
            for each_list in store_list:
                #for each node in the list
                for each_node in each_list:
                    left_height = right_height = 0
                    #print store_list
                    #print each_node, type(each_node)
                    if not each_node.isLeaf():
                        left_height= each_node.left_node.reverse_height \
                        if each_node.hasLeftChild() else None
                        right_height = each_node.right_node.reverse_height \
                        if each_node.hasRightChild() else None
                        each_node.reverse_height = max(left_height, right_height) + 1
        
        evaluate(store_op(tot_nodes))
        return self.reverse_height
    
    def revHeightDiff(self):
        """difference in reverse Height between child nodes"""
        
        #update reverse height throughout all children nodes and current node
        self.revHeight()
        
        if self.hasLeftChild() and self.hasRightChild():
            return abs(self.left_node.reverse_height - self.right_node.reverse_height)
        else:
            return self.reverse_height
    
    def find_tot_nodes(self):
        """Find total nodes from self and below
        #recursive but runs out of stack exceeding max rec depth 
        count = 1
        if self.hasLeftChild():
            count += self.left_node.find_tot_nodes()
        if self.hasRightChild():
            count += self.right_node.find_tot_nodes()
        return count
        """
        print "find_tot_nodes Start"
        master = []
        temp = deque([self])
        while len(temp) != 0:
            #print "inside find_tot_nodes loop length {} with nodes {}".format(len(temp), [i.root_node for i in temp])
            each_node = temp.popleft()
            #print "each_node is {}".format(each_node.root_node)
            if each_node.hasLeftChild():
                temp.append(each_node.left_node)
            if each_node.hasRightChild():
                temp.append(each_node.right_node)
            master.append(each_node)
        print "find_tot_nodes Done"
        return len(master)

        
        
    
    def __str__(self):
        return "Root Node %s with parent %s with left child %s right child %s" %(\
        self.root_node, self.parent_node.root_node if hasattr(self, 'parent_node') else "None",\
        (self.left_node.root_node) if hasattr(self, 'left_node') else "None", \
        (self.right_node.root_node) if hasattr(self, 'right_node') else "None")


class btree(object):
    """A Binary Search Tree Implementation.
    It can:
        - Insert a node
        - Search for a node
        - Delete a node.
        - Minor misc. utilities.
        
    """
    
    def __init__(self, root_node, node_val=None):
        """root_node is a numeric value"""
        self.size = 0
        self.treeheight = 0
        self.min_node = None
        self.max_node = None
        #root_node is node_key
        self.insert(root_node, node_val)
        self.setMaxTreeHeight()
    
    # All about setting a Node in the tree    
    def insert(self, node_key, node_val=None):
        """Insert a root node if tree is emtpy else a new node under it"""
        print "inserting..{}".format(node_key)
        if isinstance(node_key, (int, float, long)):
            new_node = bnode(node_key, value=node_val)
            
            if hasattr(self, 'root_node'):
                self.root_node.add_child_node(new_node)
            else:
                self.root_node = new_node
            
            self.size += 1
            self.min_node = self.find_min_key(self.root_node)
            self.max_node = self.find_max_key(self.root_node)
        else:
            raise Exception("Not a bnode class")
        print "done inserting.."
    #
    
    # All about searching for a Node
    @classmethod
    def get_node(cls, bnode_instance, node_key):
        """ A recursive search for node_key. Returns the Node instance
        if present else None. Can be called directly. 
        node_key: A numeric value.
        
        #a recursive solution
        if node_key == bnode_instance.root_node:
            return bnode_instance
        elif node_key < bnode_instance.root_node:
            return cls.get_node(bnode_instance.left_node, node_key) if bnode_instance.hasLeftChild() else None
        elif node_key > bnode_instance.root_node:
            return cls.get_node(bnode_instance.right_node, node_key) if bnode_instance.hasRightChild() else None
        """
        #a non recursive approach
        while node_key != bnode_instance.root_node:
            if node_key < bnode_instance.root_node:
                if bnode_instance.hasLeftChild():
                    bnode_instance = bnode_instance.left_node
                else:
                    return None
            elif node_key > bnode_instance.root_node:
                if bnode_instance.hasRightChild():
                    bnode_instance = bnode_instance.right_node
                else:
                    return None
        return bnode_instance if node_key == bnode_instance.root_node else None
    
    def __contains__(self, node_key):
        """Returns True if the specified key exists in the Tree ele
        False. 
        This way keys can be searched like:
            5 in btree1.
        node_key: A numeric value."""
        return True if self.get_node(self.root_node, node_key) != None else False
    
    def find_min_key(self, start_node):
        """Find minimum key value from given node and below"""
        root_node = start_node
        min_key = root_node.root_node
        min_node = root_node
           
        while root_node.hasLeftChild():
            root_node = root_node.left_node
            if min_key > root_node.root_node:
                min_key = root_node.root_node
                min_node = root_node
        del min_key
        return min_node
    
    def find_max_key(self, start_node):
        """Find maximum key value from given node and below"""
        root_node = start_node
        max_key = root_node.root_node
        max_node = root_node
           
        while root_node.hasRightChild():
            root_node = root_node.right_node
            if max_key < root_node.root_node:
                max_key = root_node.root_node
                max_node = root_node
        del max_key
        return max_node
    # 
    
    # All About Deleting a Node and rebalancing the Tree
    def delete(self, node_key):
        """Deletes a node from the key and adjusts the bst property"""
        def _remove(node_key):
            if node_key in self:
                #get that node
                node_obj = self.get_node(self.root_node, node_key)
                #find its parent if not root
                parent_node = node_obj.parent_node if node_obj.hasParent() else None
                        
                if node_obj.hasLeftChild() and node_obj.hasRightChild():
                    #check if subtree children are 2 or 1
                    #if 2 subtree
                    #find the minimum of the right subtree-min_right_subtree_node
                    new_node = self.find_min_key(node_obj.right_node)
                    #and remove the minimum node of the right subtree
                    min_right_parent = new_node.parent_node
                    #REMOVE Child
                    min_right_parent.remove(new_node)
                    #redirect node_objects children to new node
                    if node_obj.hasLeftChild():
                        new_node.add_child_node(node_obj.left_node)
                    if node_obj.hasRightChild():
                        new_node.add_child_node(node_obj.right_node)
                elif node_obj.isLeaf():
                    new_node = None
                else:
                    #if one child subtree, point it to the parent's parent
                    #and point parent's parent to this subtree root
                    new_node = node_obj.left_node if node_obj.hasLeftChild() \
                    else node_obj.right_node
                
                #Connect to the upper nodes
                if parent_node:
                    #REMOVE Child
                    parent_node.remove(node_obj)
                    #and swap the current nodes value with its values and key
                    parent_node.add_child_node(new_node)
                elif new_node:
                    self.root_node = new_node
                del node_obj
            else:
                raise Exception("No such node present")
        
        _remove(node_key)
        self.min_node = self.find_min_key(self.root_node)
        self.max_node = self.find_max_key(self.root_node)
        self.size -= 1
        return
    #
    
    # All About Getting the Max Tree Height of the Tree and Settign it
    # 
    def getMaxTreeHeight(self):
        """calculate the maximum height of tree starting from tree root"""
        self.root_node.refreshHeight()  #refresh height from root to leaves
        self.treeheight = self.root_node.getMaxHeight()
        return self.treeheight
    
    @classmethod
    def imprint_height(cls, bnode_instance, tree_height):
        """
        
        The idea is to have each node in the btree have the same information 
        i.e. the maximum tree height of that btree so cutting back to recalculating 
        the same each time;
        
        This function is called from btree and is recursive.
        should be classmethod.
        
        Given a bnode class instance and the maximum tree height:
            (tree height = self.treeheight)
            
        1. Go through each node in the tree
        2. Find its left and right child nodes and go back to step 1
        3. Set a new class instance attribute 'maxtreeheight'
        on bnode instance with value tree height.
        """
        
        if not bnode_instance.isLeaf():
            if bnode_instance.hasLeftChild():
                cls.imprint_height(bnode_instance.left_node, tree_height)
            if bnode_instance.hasRightChild():
                cls.imprint_height(bnode_instance.right_node, tree_height)
        setattr(bnode_instance, 'maxtreeheight', tree_height)
        return
    
    
    def setMaxTreeHeight(self):
        """ Sets the maximum height attribute in each node in the tree
        so each node knows the current maximum height."""
        self.imprint_height(self.root_node, self.getMaxTreeHeight())
    #


class AvlTree(btree):
    """An AVL Tree"""
    def __init__(self, root_node, node_val=None):
        """initialize the AVL tree using BST property"""
        super(type(self), self).__init__(root_node, node_val=node_val)
        self.rev_height = 0
    
    def getReverseHeight(self):
        """gets the reverse tree height from leaf to root node"""
        self.rev_height = self.root_node.revHeight()
        return self.rev_height
    
    @classmethod
    def imprintReverseHeight(cls, bnode_instance, tree_rev_height):
        """imprints the given reverse tree height on each node"""
        if not bnode_instance.isLeaf():
            if bnode_instance.hasLeftChild():
                cls.imprint_height(bnode_instance.left_node, tree_rev_height)
            if bnode_instance.hasRightChild():
                cls.imprint_height(bnode_instance.right_node, tree_rev_height)
        setattr(bnode_instance, 'max_rev_height', tree_rev_height)
        return
    
    def setMaxRevHeight(self):
        """sets universal maximum height from leaf to root per node"""
        self.imprintReverseHeight(self.root_node, self.getReverseHeight())
    
    ## Rotation operation
    @classmethod
    def left_rotate(cls, node):
        """
        Left Rotation of node:
        -------------------------
        Remove node' parent association if any.
        Remove node' right child 
        Remove parent association with right child
        Set right child's left child as new right child of node.
        Remove associate between right child and its left child.
        Set right child as root and node as left child of root.
        Relink root node' parent associate if any.
        return root node as new node
        """
        #Remove node' parent association if any.
        if node.hasParent():
            parent = node.parent_node
            parent.remove(node)
        else:
            parent = None
        
        #Remove node' right child
        right_child = node.right_node
        node.remove(right_child)
        
        #Set right child's left child as new right child of node.
        if right_child.hasLeftChild():
            right_left = right_child.left_node
            #Remove associate between right child and its left child.
            right_child.remove(right_left)
            node.add_child_node(right_left)
        
        #Set right child as root and node as left child of root.
        right_child.add_child_node(node)
        
        #Relink root node' parent associate if any.
        if parent:
            parent.add_child_node(right_child)
        
        #return root node as new node
        return right_child
    
    @classmethod
    def right_rotate(cls, node):
        """
        Right Rotation of node:
        -------------------------
        Remove node' parent association if any.
        Remove node' left child 
        Remove parent association with left child
        Set left child's right child as new left child of node.
        Remove associate between left child and its right child.
        Set left child as root and node as right child of root.
        Relink root node' parent associate if any.
        return root node as new node
        """
        #Remove node' parent association if any.
        if node.hasParent():
            parent = node.parent_node
            parent.remove(node)
        else:
            parent = None
        
        #Remove node' left child
        left_child = node.left_node
        node.remove(left_child)
        
        #Set left child's right child as new left child of node.
        if left_child.hasRightChild():
            left_right = left_child.right_node
            #Remove associate between left child and its right child.
            left_child.remove(left_right)
            node.add_child_node(left_right)
        
        #Set left child as root and node as right child of root.
        left_child.add_child_node(node)
        
        #Relink root node' parent associate if any.
        if parent:
            parent.add_child_node(left_child)
        
        #return root node as new node
        return left_child
    
    @classmethod
    def rotate(cls, node):
        """Rotates current node to adjust AVL property"""
        if node.hasLeftChild() and node.hasRightChild():
            if (node.left_node.reverse_height - node.right_node.reverse_height) > 1:
                print "right rotation"
                node = cls.right_rotate(node)
            elif (node.right_node.reverse_height - node.left_node.reverse_height) > 1:
                print "left rotation"
                node = cls.left_rotate(node)
        elif not node.hasLeftChild():
            print "left rotation"
            node = cls.left_rotate(node)
        elif not node.hasRightChild():
            print "right rotation"
            node = cls.right_rotate(node)
        return node
    ##
    
    ## Balancing operation
    @classmethod
    def _rebalance(cls, node):
        #if leaf node return
        #else rotate if height difference
        #update revHeight
        #recurse _rebalance to child nodes
        done = []
        temp = deque([node])
        print "REBALANCE STARTS"
        while temp:
            each_node = temp.popleft()
            #print "In REBALANCE with each node {}".format(each_node.root_node)
            #if each_node.root_node in done:
                #print "{} REPEATS! ALRDY in done list {}".format(each_node.root_node, done)
            if each_node.revHeightDiff() > 1:
                each_node = cls.rotate(node)
                #this is a new node. reval reverse height
                each_node.revHeight()
            if each_node.hasLeftChild():
                temp.append(each_node.left_node)
            if each_node.hasRightChild():
                temp.append(each_node.right_node)
            done.append(each_node.root_node)
            #print "temp list {}".format([i.root_node for i in temp])
        print "REBALANCE ENDS"
        return
    
    def balance(self):
        print "BALANCE FUNC START"
        print "pre condition check"
        while self.root_node.revHeightDiff() > 1:
            print "post condition check"
            #while root node unbalanced
            print "rotating"
            self.root_node = self.rotate(self.root_node)
            print "rotation done"
            #print "calculating rev Height in balance..."
            self.root_node.revHeight()
            #go down
            if self.root_node.hasLeftChild():
                self._rebalance(self.root_node.left_node)
            if self.root_node.hasRightChild():
                self._rebalance(self.root_node.right_node)
            print "self.size {}".format(self.size)
            if self.size < 4:
                #print "BALANCE FUNC: Breaking for size < 4"
                break
        print "BALANCE FUNC END"
        return
    ##
    
    def _innerRotate_insertPostOp(self, leaf_node):
        """Swap pre Rotation. Useful for AvlTree"""
        if leaf_node.hasParent() and leaf_node.isLeaf():
            node = leaf_node.parent_node
            #inner right rotate
            if leaf_node.isLeftChild() and node.hasParent() \
            and node.hasLeftChild() and (not node.hasRightChild()) and node.isRightChild():
                self.right_rotate(node)
            elif leaf_node.isRightChild() and node.hasParent() \
            and node.hasRightChild() and (not node.hasLeftChild()) and node.isLeftChild():
                #inner left rotate
                self.left_rotate(node)
    
    def _optimize_leaf(self):
        """Find leaves that allow 2 rotation principle"""
        leaves = []
        temp = deque([self.root_node])
        while temp:
            print "inside _optimize_leaf LOOP"
            each_node = temp.popleft()
            if each_node.isLeaf():
                leaves.append(each_node)
            if each_node.hasLeftChild():
                temp.append(each_node.left_node)
            if each_node.hasRightChild():
                temp.append(each_node.right_node)
        print "LEAVES {}".format([i.root_node for i in leaves])
        for each_leaf in leaves:
            self._innerRotate_insertPostOp(each_leaf)
    
    # post op utility after inserting, deleting, modification
    def _postop(self):
        #print "refreshing height post op AVL"
        #self.root_node.refreshHeight()
        #print "done"
        print "calculating post op AVL revHeight.."
        self.root_node.revHeight()
        print "postop AVL revHeight Calc done"
        print "ENTERING optimize Leaf"
        #self._optimize_leaf()
        print "ENDED optimize Leaf"
        self.balance()
        self.root_node.refreshHeight()
        self.setMaxTreeHeight()
        self.setMaxRevHeight()
    ##
    
    #Delete operation
    def AvlDelete(self, node_key):
        """
        Performs balanced deletion.
        node_key: A key to insert. A numeric type.
        
        Deletes a key like typical bst operation.
        checks for invariance on structure.
        performs subtree balancing where left-right tree height 
        differs by more than 1.
        """
        self.delete(node_key)
        print "entering AVL Insert post op"
        self._postop()
    
    #Insert operation
    def AvlInsert(self, node_key, node_val=None):
        """Performs balanced Insertion.
        node_key: A key to insert. A numeric type.
        node_val: The value of the key. A string type.
        
        Inserts the key.
        checks for invariance on structure.
        performs subtree balancing where left-right tree height 
        differs by more than 1.
        """
        print "entered AVL inserting"
        self.insert(node_key, node_val=node_val)
        print "\n entering AVL Insert post op\n"
        self._postop()
    
    def AvlInsertBatch(self, batch):
        """Insert in batch only node_keys without their values"""
        #[self.AvlInsert(node_key) for node_key in batch]
        map(self.AvlInsert, batch)
    
    def _AvlAddChild(self, node):
        """
        Add an alien child node of another tree.
        Used in AvlMerge.
        """
        temp = deque()
        temp.append(node)
        while temp:
            each_node = temp.popleft()
            if each_node.hasLeftChild():
                temp.append(each_node.left_node)
            if each_node.hasRightChild():
                temp.append(each_node.right_node)
            self.AvlInsert(each_node.root_node)
    
    def AvlMerge(self, another_tree):
        """Merge Two trees Unique nodes.
        This will merge the root of another AVL Tree with current Tree 
        and rebalance. O(nlogn) Operation"""
        if isinstance(another_tree, AvlTree):
            alien_root = another_tree.root_node
            self._AvlAddChild(alien_root)


#for quick testing purposes
if __name__ == "__main__":
    from numpy.random import randint
    
    def gen_unique_num(r):
        t = []
        for _ in xrange(r):
            a = randint(1, 1000000000)
            if a not in t:
                t.append(a)
        return t
    
    atree = AvlTree(80, 'FlightA')
    
    atree.AvlInsert(257)
    atree.AvlInsert(932)
    
    atree.AvlInsert(225)
    atree.AvlInsert(275)
    
    atree.AvlInsert(991)
    atree.AvlInsert(274)

    
    atree.AvlInsert(656)
    
    atree.AvlInsert(885)
    
    atree.AvlInsert(574)
    
    #atree.AvlInsert(600)
    #atree.AvlInsert(564)
    
    ctree = AvlTree(600)
    ctree.AvlInsert(564)
    atree.AvlMerge(ctree)
    atree.AvlDelete(885)
    
    #an eg from MIT class
    sucker = AvlTree(41)
    sucker.AvlInsert(20)
    sucker.AvlInsert(65)
    sucker.AvlInsertBatch([11, 26, 50, 23, 29, 55])
    
    
    dt = AvlTree(80)
    dt.AvlInsert(101)
    dt.AvlInsert(90)