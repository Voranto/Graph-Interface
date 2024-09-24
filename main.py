import time
import pygame
from sys import exit
import random
from random import choice
import heapq
import math


width = 1400
height = 800

#SOLVING THE GRAPH



pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width+3,height+3))
pygame.display.set_caption("MAZE GENERATION")
my_font = pygame.font.SysFont('Comic Sans MS', 30)



class Button:
    def __init__(self,x,y,width,height,color,text,image):
        self.rect = pygame.Rect(toolbar.rect.x + x,toolbar.rect.y + y, width, height)
        self.color = color
        if image != "":
            self.icon = pygame.image.load("icons/"+image)
            
            self.iconrect = self.icon.get_rect()
            self.icon = pygame.transform.scale(self.icon,(width-10,height-10))
            self.iconrect.x += toolbar.rect.x + x + 5
            self.iconrect.y += toolbar.rect.y + y + 5
        else:
            self.icon = ""
        self.mode = text
        self.font = pygame.font.Font(None, 36)
    
    def draw(self,screen):
        pygame.draw.rect(screen,self.color,self.rect)
        if self.icon != "":
            screen.blit(self.icon, self.iconrect)
        
    def is_hovering(self,mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self,mouse_pos,mouse_clicked):
        return mouse_clicked and self.is_hovering(mouse_pos)
    
class Toolbar:
    def __init__(self,x,y,height,width,color,border_color,border_width):
        self.Buttons = []
        self.rect = pygame.Rect(x, y, width, height)
        self.color =  color
        self.border_color = border_color
        self.border_width = border_width
        self.currmode = None
    
    def render(self,screen):
        pygame.draw.rect(screen,self.border_color,pygame.Rect(self.rect.x-self.border_width,self.rect.y-self.border_width,self.rect.width+2*self.border_width,self.rect.height+2*self.border_width))
        pygame.draw.rect(screen,self.color,self.rect)
        
        self.process_buttons(screen)
    
    def process_buttons(self,screen):
        for button in self.Buttons:
            #gestion de colores
            if button.mode != self.currmode:
                button.color = pygame.Color(200,200,200)
                if button.is_hovering(pygame.mouse.get_pos()):
                    button.color = pygame.Color(150,150,150)
            else:
                button.color = pygame.Color(100,100,100)
            
            if button.is_clicked(pygame.mouse.get_pos(),pygame.mouse.get_pressed()[0]):
                if button.mode == "cleargraph":
                    main_graph.nodes = []
                if button.mode != "solvegraph" and self.currmode == "solvegraph":
                    solveend.bordercolor = "Black"
                    solvestart.bordercolor = "Black"
                if button.mode == "solvegraph" and main_graph.nodes:
                    resetsolve()
                    if solvestart and solveend:
                        solveend.bordercolor = "Black"
                        solvestart.bordercolor = "Black"
                    self.currmode = button.mode
                    button.color = pygame.Color(100,100,100)
                elif button.mode == "solvegraph" and not main_graph.nodes:
                    button.color = pygame.Color(255,0,0)
                    print("GRAPH DOES NOT EXIST")
                else:
                    self.currmode = button.mode
                    button.color = pygame.Color(100,100,100)
                
            button.draw(screen)
            

class Node:
    def __init__(self,val,x,y):
        self.value = val
        self.edges = []
        self.path = []
        self.centerpos = (x,y)
        self.bordercolor = "Black"

    
    def draw(self,screen):
        pygame.draw.circle(screen,self.bordercolor,self.centerpos,20,2)
        pygame.draw.circle(screen,"White",self.centerpos,18)
        text_surface = pygame.transform.scale(my_font.render(str(self.value), False, (0, 0, 0)),(20,40))
        screen.blit(text_surface,(self.centerpos[0] - 10 ,self.centerpos[1]-20 ))
        
                
class Graph:
    def __init__(self):
        self.nodes = []
        
    def render(self,screen):
        for curr in self.nodes:
            for edge in curr.edges:
                pygame.draw.line(screen,"Black",curr.centerpos,edge.centerpos,1)
        for curr in self.nodes:
            curr.draw(screen)
        

toolbar = Toolbar(width-105,5,height-10,100,"White","Black",3)
toolbar.Buttons.append(Button(10,10,80,80,pygame.Color(200,200,200),"addnode","add_node.png",))
toolbar.Buttons.append(Button(10,100,80,80,pygame.Color(200,200,200),"deletenode","delete_node.png",))
toolbar.Buttons.append(Button(10,190,80,80,pygame.Color(200,200,200),"addedges","add_edges.png",))
toolbar.Buttons.append(Button(10,280,80,80,pygame.Color(200,200,200),"randomgraph","random_graph.png",))
toolbar.Buttons.append(Button(10,370,80,80,pygame.Color(200,200,200),"movenodes","move_nodes.png",))
toolbar.Buttons.append(Button(10,460,80,80,pygame.Color(200,200,200),"solvegraph","solve_graph.png",))
toolbar.Buttons.append(Button(10,550,80,80,pygame.Color(200,200,200),"cleargraph","clear_graph.png",))



solvestart = None
solveend = None
def resetsolve():
    global solvestart,solveend
    solvestart = None
    solveend = None

movingnode = None
main_graph = Graph()
nodes_to_add = -1
edgestart = None
edgeend = None
c = 0
def process_nodes(mode,currpos):
    global c,main_graph
    if currpos[0] < width - 100:
        if mode == "addnode":
            main_graph.nodes.append(Node(c, currpos[0],currpos[1]))
            c+=1
            
            
        elif mode == "deletenode":
            #iteramos a traves de todos los nodos
            for node in main_graph.nodes[::-1]:
                #si el raton toca el nodo quitarlo ambos de el grafo, como todos los edges conectados a el
                if abs(currpos[0] - node.centerpos[0]) ** 2 +  abs(currpos[1] - node.centerpos[1]) ** 2 < 400:
                    main_graph.nodes.remove(node)
                    for node2 in main_graph.nodes:
                        if node in node2.edges:
                            node2.edges.remove(node)
                    break
    
import random

def distance(a,b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def generate_random_graph(node_count, max_extra_edges=10):
    global c, main_graph
    
    # Step 1: Generate random nodes
    for i in range(node_count):
        x, y = random.randint(20, width - 120), random.randint(20, height - 20)
        main_graph.nodes.append(Node(c, x, y))
        c += 1
    
    # Step 2: Generate the MST (to ensure connectivity)
    remaining_nodes = main_graph.nodes[:]
    connected_nodes = [remaining_nodes.pop(0)]  # Start with the first node
    
    while remaining_nodes:
        # Randomly select a node from the connected graph
        current_node = random.choice(connected_nodes)
        
        # Find the nearest unconnected node
        next_node = min(remaining_nodes, key=lambda node: distance(current_node.centerpos, node.centerpos))
        
        # Connect the two nodes
        current_node.edges.append(next_node)
        next_node.edges.append(current_node)
        
        # Move the newly connected node to the connected list
        connected_nodes.append(next_node)
        remaining_nodes.remove(next_node)
    
    # Step 3: Add random extra edges
    extra_edges = 0
    while extra_edges < max_extra_edges:
        node1 = random.choice(main_graph.nodes)
        node2 = random.choice(main_graph.nodes)
        
        # Avoid adding an edge between the same node or adding duplicate edges
        if node1 != node2 and node2 not in node1.edges:
            node1.edges.append(node2)
            node2.edges.append(node1)
            extra_edges += 1
    
    print("Random graph generated with", node_count, "nodes and", extra_edges, "extra edges.")
     
    
def process_edges(mode,currpos,isclicked):
    global edgestart,edgeend,nodes_to_add,c,movingnode,solvestart,solveend
    if mode == "addedges":
        if edgestart and not edgeend:
            pygame.draw.line(screen,"Black",edgestart.centerpos,currpos,2)
        if isclicked:
            flag = False
            for node in main_graph.nodes[::-1]:
                #si el raton toca el nodo quitarlo ambos de el grafo, como todos los edges conectados a el
                if abs(currpos[0] - node.centerpos[0]) ** 2 +  abs(currpos[1] - node.centerpos[1]) ** 2 < 400:
                    flag = True
                    if edgestart == None:
                        edgestart = node
                        node.bordercolor = "Red"
                    elif edgestart != node and edgestart not in node.edges:
                        edgeend = node
                        edgestart.edges.append(edgeend)
                        edgeend.edges.append(edgestart)
                        edgestart.bordercolor = "Black"
                        edgestart = None
                        edgeend = None
                        
                    break
            if not flag:
                if edgestart:
                    edgestart.bordercolor = "Black"
                edgestart = None
    elif mode == "movenodes":
        if not movingnode and  mouse_pressed:
            for node in main_graph.nodes[::-1]:
                #si el raton toca el nodo quitarlo ambos de el grafo, como todos los edges conectados a el
                if abs(currpos[0] - node.centerpos[0]) ** 2 +  abs(currpos[1] - node.centerpos[1]) ** 2 < 400:
                    movingnode = node
                    break
        elif not mouse_pressed:
            movingnode = None
        if movingnode:
            movingnode.centerpos = currpos
    elif mode == "randomgraph" and nodes_to_add == -1:
        nodes_to_add = int(input("HOW MANY NODES DO YOU WANT TO ADD: "))   
        generate_random_graph(nodes_to_add, max_extra_edges=10)
        mode = None
    elif nodes_to_add != -1:
        mode = None
        nodes_to_add = -1
        
    #SOLVE THE GRAPH
    elif mode == "solvegraph":
        text_surface = my_font.render("Please select starting and ending nodes", False, (0, 0, 0))
        screen.blit(text_surface,(20,20))
        
        if isclicked:
            for node in main_graph.nodes[::-1]:
                #si el raton toca el nodo quitarlo ambos de el grafo, como todos los edges conectados a el
                if abs(currpos[0] - node.centerpos[0]) ** 2 +  abs(currpos[1] - node.centerpos[1]) ** 2 < 400:
                    if not solvestart:
                        solvestart = node
                        solvestart.bordercolor = "Red"
                    elif solvestart != node:
                        if solveend:
                            solveend.bordercolor = "Black"
                        solveend = node
                        solveend.bordercolor = "Green"
                    break
        
        if solvestart and solveend:
            last = bfs()
            if last == solveend:
                for i in range(1,len(last.path)):
                    pygame.draw.line(screen,"darkgreen",last.path[i-1].centerpos,last.path[i].centerpos,10)
    return mode   
        

def print_graph():
    for node in main_graph.nodes:
        print("-----------------------------------------------")
        print("Node is: ", node.value)
        print("Edges of previous node: ", [edge.value for edge in node.edges])

edit_node_flag = False
mouse_pressed = False

def bfs():
    stack = [solvestart]
    visited = set([solvestart])
    solvestart.path = [solvestart]
    while stack:  
        curr = stack.pop(0)
        curr.visited = True
        if curr == solveend:
            break
        x,y = curr.centerpos
        for neighbor in curr.edges:
            if neighbor not in visited and neighbor not in stack:
                if neighbor.path == []:
                    neighbor.path.append(neighbor)
                    for camino in curr.path:
                        neighbor.path.append(camino)
                visited.add(neighbor)
                stack.append(neighbor)
    return curr

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not mouse_pressed:  # Detect the first press
                mouse_pressed = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False  # Reset the state when mouse is released
                
    screen.fill("Gray")
    toolbar.currmode = process_edges(toolbar.currmode,pygame.mouse.get_pos(),pygame.mouse.get_pressed()[0])
    if pygame.mouse.get_pressed()[0] and not edit_node_flag:
        process_nodes(toolbar.currmode,pygame.mouse.get_pos())
        edit_node_flag = True
    
    
    elif not pygame.mouse.get_pressed()[0]:
        edit_node_flag = False
    
    
    main_graph.render(screen)
    
    #print_graph()
    #draw buttons
    toolbar.render(screen)
            
    pygame.display.update()
    
    
    
    
    
    
