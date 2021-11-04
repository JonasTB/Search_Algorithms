import sys
from settings import *
from buttons import *
from bfs_class import *
from dfs_class import *
from astar_class import *
from dijkstra_class import *
from greedy_class import *
from visualize_path_class import *
from maze_class import *

pygame.init()

class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'Menu Principal'
        self.algorithm_state = ''
        self.grid_square_length = 24
        self.load()
        self.start_end_checker = 0
        self.mouse_drag = 0

        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None

        self.wall_pos = wall_nodes_coords_list.copy()

        self.maze = Maze(self, self.wall_pos)

        self.bfs_button = Buttons(self, WHITE, 228, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Busca por Largura')
        self.dfs_button = Buttons(self, WHITE, 448, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Busca por Profundidade')
        self.astar_button = Buttons(self, WHITE, 668, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'A-Estrela')
        self.dijkstra_button = Buttons(self, WHITE, 888, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'Custo Uniforme')
        self.greedy_button = Buttons(self, WHITE, 1108, MAIN_BUTTON_Y_POS, MAIN_BUTTON_LENGTH, MAIN_BUTTON_HEIGHT, 'BGME')
        
        self.start_end_node_button = Buttons(self, REDFLA, 20, START_END_BUTTON_HEIGHT, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Inicio/Fim')
        self.wall_node_button = Buttons(self, REDFLA, 20, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT + BUTTON_SPACER, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Parede')
        self.reset_button = Buttons(self, REDFLA, 20, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT*2 + BUTTON_SPACER*2, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Resetar')
        self.start_button = Buttons(self, REDFLA, 20, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT*3 + BUTTON_SPACER*3, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Vizualizar Caminho')
        self.main_menu_button = Buttons(self, REDFLA, 20, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT * 4 + BUTTON_SPACER * 4, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Menu Principal')
        self.maze_generate_button = Buttons(self, REDFLA, 20, START_END_BUTTON_HEIGHT + GRID_BUTTON_HEIGHT * 5 + BUTTON_SPACER * 5, GRID_BUTTON_LENGTH, GRID_BUTTON_HEIGHT, 'Gerar Labirinto')
    def run(self):
        while self.running:
            if self.state == 'Menu Principal':
                self.main_menu_events()
            if self.state == 'grid window':
                self.grid_events()
            if self.state == 'draw S/E' or self.state == 'draw walls':
                self.draw_nodes()
            if self.state == 'start visualizing':
                self.execute_search_algorithm()
            if self.state == 'aftermath':
                self.reset_or_main_menu()

        pygame.quit()
        sys.exit()

#################################### FUNCTIONS #########################################
    

    def load(self):
        self.main_menu_background = pygame.image.load('gabigol.jpg')
        self.grid_background = pygame.image.load('Flamengo.png') 
        self.main_menu_background = pygame.transform.scale(self.main_menu_background, (1920, 800))
        self.grid_background = pygame.transform.scale(self.grid_background, (250, 325))
# Desenhar texto
    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(words, False, colour)
        text_size = text.get_size()
        if centered:
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(text, pos)

# Menu Principal
    def sketch_main_menu(self):
        self.screen.blit(self.main_menu_background, (0, 0))

        # Draw Buttons
        self.bfs_button.draw_button(REDFLA)
        self.dfs_button.draw_button(REDFLA)
        self.astar_button.draw_button(REDFLA)
        self.dijkstra_button.draw_button(REDFLA)
        self.greedy_button.draw_button(REDFLA)

# Configuração do mapa
    def sketch_hotbar(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, WHITE, (0, 0, 1500, 768), 0)
        self.screen.blit(self.grid_background, (0, 0))

    def sketch_grid(self):
        # adicionar bordas
        pygame.draw.rect(self.screen, ALICE, (240, 0, WIDTH, HEIGHT), 0)
        pygame.draw.rect(self.screen, REDFLA, (264, 24, GRID_WIDTH, GRID_HEIGHT), 0)

        # desenha mapa
        # 30x52 mapa
        for x in range(52):
            pygame.draw.line(self.screen, ALICE, (GS_X + x*self.grid_square_length, GS_Y),
                            (GS_X + x*self.grid_square_length, GE_Y))
        for y in range(30):
            pygame.draw.line(self.screen, ALICE, (GS_X, GS_Y + y*self.grid_square_length),
                            (GE_X, GS_Y + y*self.grid_square_length))

    

    def sketch_grid_buttons(self):
        # desenhar butões
        self.start_end_node_button.draw_button(STEELBLUE)
        self.wall_node_button.draw_button(STEELBLUE)
        self.reset_button.draw_button(STEELBLUE)
        self.start_button.draw_button(STEELBLUE)
        self.main_menu_button.draw_button(STEELBLUE)
        self.maze_generate_button.draw_button(STEELBLUE)

    # Funçãos pros botoes
    # checa o estado do butão quando clicado e faz um hover ao passar o mouse.
    def grid_window_buttons(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_end_node_button.isOver(pos):
                self.state = 'draw S/E'
            elif self.wall_node_button.isOver(pos):
                self.state = 'draw walls'
            elif self.reset_button.isOver(pos):
                self.execute_reset()
                self.maze = Maze(self, self.wall_pos)
                # self.maze.generateSolid2()
            elif self.start_button.isOver(pos):
                self.state = 'start visualizing'
            elif self.main_menu_button.isOver(pos):
                self.back_to_menu()
                self.maze = Maze(self, self.wall_pos)

            elif self.maze_generate_button.isOver(pos):
                self.state = 'draw walls'
                # self.wall_pos = wall_nodes_coords_list.copy()
                self.maze = Maze(self, self.wall_pos)
                self.maze.generateSolid()
                
                self.state = 'draw S/E'

        # hoveer
        if event.type == pygame.MOUSEMOTION:
            if self.start_end_node_button.isOver(pos):
                self.start_end_node_button.colour = REDFLA
            elif self.wall_node_button.isOver(pos):
                self.wall_node_button.colour = REDFLA
            elif self.reset_button.isOver(pos):
                self.reset_button.colour = REDFLA
            elif self.start_button.isOver(pos):
                self.start_button.colour = REDFLA
            elif self.main_menu_button.isOver(pos):
                self.main_menu_button.colour = REDFLA
            elif self.maze_generate_button.isOver(pos):
                self.maze_generate_button.colour = REDFLA
            else:
                self.start_end_node_button.colour, self.wall_node_button.colour, self.reset_button.colour, \
                self.start_button.colour, self.main_menu_button.colour, self.maze_generate_button.colour = \
                    STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE

    def grid_button_keep_colour(self):
        if self.state == 'draw S/E':
            self.start_end_node_button.colour = REDFLA

        elif self.state == 'draw walls':
            self.wall_node_button.colour = REDFLA

    def execute_reset(self):
        self.start_end_checker = 0

        # Início e fim das coordenadas dos nó
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None
        self.end_node_y = None
     
        # Wall Nodes List 
        # self.maze.redrawGrid()
        print(self.wall_pos)
        print('----------')
        self.wall_pos = wall_nodes_coords_list.copy()
        print(self.wall_pos)

        # Mudar estados
        self.state = 'grid window'

    def back_to_menu(self):
        self.start_end_checker = 0

        # Início e fim das coordenadas dos nó
        self.start_node_x = None
        self.start_node_y = None
        self.end_node_x = None
        self.end_node_y = None
        
        self.wall_pos = wall_nodes_coords_list.copy()

        # Mudar estados
        self.state = 'Menu Principal'


#################################### FUNCTIONS #########################################

##### Menu Funções

    def main_menu_events(self):
        # Draw Background
        pygame.display.update()
        self.sketch_main_menu()
        # self.draw_text('sfdfdsf', self.screen, [800, 600], 28, WHITE, FONT, centered=False)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.bfs_button.isOver(pos):
                    self.algorithm_state = 'bfs'
                    self.state = 'grid window'
                if self.dfs_button.isOver(pos):
                    self.algorithm_state = 'dfs'
                    self.state = 'grid window'
                if self.astar_button.isOver(pos):
                    self.algorithm_state = 'astar'
                    self.state = 'grid window'
                if self.dijkstra_button.isOver(pos):
                    self.algorithm_state = 'dijkstra'
                    self.state = 'grid window'
                if self.greedy_button.isOver(pos):
                    self.algorithm_state = 'greedy'
                    self.state = 'grid window'

            if event.type == pygame.MOUSEMOTION:
                if self.bfs_button.isOver(pos):
                    self.bfs_button.colour = REDFLA
                elif self.dfs_button.isOver(pos):
                    self.dfs_button.colour = REDFLA
                elif self.astar_button.isOver(pos):
                    self.astar_button.colour = REDFLA
                elif self.dijkstra_button.isOver(pos):
                    self.dijkstra_button.colour = REDFLA
                elif self.greedy_button.isOver(pos):
                    self.greedy_button.colour = REDFLA
                else:
                    self.bfs_button.colour, self.dfs_button.colour, self.astar_button.colour, self.dijkstra_button.colour, \
                    self.greedy_button.colour = WHITE, WHITE, WHITE, WHITE, WHITE

##### PLAYING STATE FUNCTIONS #####

    def grid_events(self):
        #print(len(wall_nodes_coords_list))
        self.sketch_hotbar()
        self.sketch_grid()
        self.sketch_grid_buttons()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            pos = pygame.mouse.get_pos()

            # Grid button function from Helper Functions
            self.grid_window_buttons(pos, event)

##### DRAWING STATE FUNCTIONS #####
    def draw_nodes(self):

        self.grid_button_keep_colour()
        self.sketch_grid_buttons()
        pygame.display.update()
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.grid_window_buttons(pos, event)

            if pos[0] > 264 and pos[0] < 1512 and pos[1] > 24 and pos[1] < 744:
                x_grid_pos = (pos[0] - 264) // 24
                y_grid_pos = (pos[1] - 24) // 24
                #print('GRID-COORD:', x_grid_pos, y_grid_pos)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_drag = 1

                    if self.state == 'draw S/E' and self.start_end_checker < 2:

                        if self.start_end_checker == 0 and (x_grid_pos+1, y_grid_pos+1) not in self.wall_pos:
                            node_colour = YELLOW
                            self.start_node_x = x_grid_pos + 1
                            self.start_node_y = y_grid_pos + 1
                            # print(self.start_node_x, self.start_node_y)
                            self.start_end_checker += 1
                            
                        elif self.start_end_checker == 1 and (x_grid_pos+1, y_grid_pos+1) != (self.start_node_x, self.start_node_y) and (x_grid_pos+1, y_grid_pos+1) not in self.wall_pos:
                            node_colour = PINK
                            self.end_node_x = x_grid_pos + 1
                            self.end_node_y = y_grid_pos + 1
                            # print(self.end_node_x, self.end_node_y)
                            self.start_end_checker += 1

                        else:
                            continue

                        pygame.draw.rect(self.screen, node_colour, (264 + x_grid_pos * 24, 24 + y_grid_pos * 24, 24, 24), 0)

                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_drag = 0

                if self.mouse_drag == 1:

                    if self.state == 'draw walls':
                        if (x_grid_pos + 1, y_grid_pos + 1) not in self.wall_pos \
                                and (x_grid_pos + 1, y_grid_pos + 1) != (self.start_node_x, self.start_node_y) \
                                and (x_grid_pos + 1, y_grid_pos + 1) != (self.end_node_x, self.end_node_y):
                            pygame.draw.rect(self.screen, BLACK, (264 + x_grid_pos * 24, 24 + y_grid_pos * 24, 24, 24), 0)
                            self.wall_pos.append((x_grid_pos + 1, y_grid_pos + 1))
                        # print(len(self.wall_pos))

                for x in range(52):
                    pygame.draw.line(self.screen, ALICE, (GS_X + x * self.grid_square_length, GS_Y),
                                     (GS_X + x * self.grid_square_length, GE_Y))
                for y in range(30):
                    pygame.draw.line(self.screen, ALICE, (GS_X, GS_Y + y * self.grid_square_length),
                                     (GE_X, GS_Y + y * self.grid_square_length))

#################################### FUNCTIONS FOR VIEW #########################################

    def execute_search_algorithm(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        #print(self.start_node_x, self.start_node_y)
        #print(self.end_node_x, self.end_node_y)

        ### BFS ###

        if self.algorithm_state == 'bfs':
            self.bfs = BreadthFirst(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                self.bfs.bfs_execute()

            # Make Object for new path
            if self.bfs.route_found:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, self.bfs.route, [])
                self.draw_path.get_path_coords()
                self.draw_path.draw_path()

            else:
                self.draw_text('Rota não Encontrada', self.screen, [768,384], 50, RED, FONT, centered = True)

        ### DFS ###

        elif self.algorithm_state == 'dfs':
            self.dfs = DepthFirst(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                self.dfs.dfs_execute()

            # Make Object for new path
            if self.dfs.route_found:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, self.dfs.route, [])
                self.draw_path.get_path_coords()
                self.draw_path.draw_path()

            else:
                self.draw_text('Rota não Encontrada', self.screen, [768,384], 50, RED, FONT, centered = True)

        ### A-STAR ###

        elif self.algorithm_state == 'astar':
            self.astar = AStar(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                self.astar.astar_execute()

            if self.astar.route_found:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, None, self.astar.route)
                self.draw_path.draw_path()

            else:
                self.draw_text('Rota não Encontrada', self.screen, [768, 384], 50, RED, FONT, centered=True)

        ### DIJKSTRA ###

        elif self.algorithm_state == 'dijkstra':
            self.dijkstra = Dijkstra(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                self.dijkstra.dijkstra_execute()

            if self.dijkstra.route_found:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, None, self.dijkstra.route)
                self.draw_path.draw_path()

            else:
                self.draw_text('Rota não Encontrada', self.screen, [768, 384], 50, RED, FONT, centered=True)

        # Sweet Tooth

        elif self.algorithm_state == 'greedy':
            self.greedy = Greedy(self, self.start_node_x, self.start_node_y, self.end_node_x, self.end_node_y, self.wall_pos)

            if self.start_node_x or self.end_node_x is not None:
                self.greedy.greedy_execute()

            if self.greedy.route_found:
                self.draw_path = VisualizePath(self.screen, self.start_node_x, self.start_node_y, None, self.greedy.route)
                self.draw_path.draw_path()

            

            else:
                self.draw_text('Rota não Encontrada', self.screen, [768, 384], 50, RED, FONT, centered=True)

        pygame.display.update()
        self.state = 'aftermath'

#################################### AFTERMATH FUNCTIONS #########################################

    def reset_or_main_menu(self):
        self.sketch_grid_buttons()
        pygame.display.update()

        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEMOTION:
                if self.start_end_node_button.isOver(pos):
                    self.start_end_node_button.colour = REDFLA
                elif self.wall_node_button.isOver(pos):
                    self.wall_node_button.colour = REDFLA
                elif self.reset_button.isOver(pos):
                    self.reset_button.colour = REDFLA
                elif self.start_button.isOver(pos):
                    self.start_button.colour = REDFLA
                elif self.main_menu_button.isOver(pos):
                    self.main_menu_button.colour = REDFLA
                else:
                    self.start_end_node_button.colour, self.wall_node_button.colour, self.reset_button.colour, self.start_button.colour, self.main_menu_button.colour = STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE, STEELBLUE

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.reset_button.isOver(pos):
                    self.execute_reset()
                elif self.main_menu_button.isOver(pos):
                    self.back_to_menu()





























