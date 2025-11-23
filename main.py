import os
import sys
import getopt
import osmnx as ox
import matplotlib.pyplot as plt


def usage():
    print("OPTIONS")
    print("-h --help - display this help menu")
    print("-d --download - download an area")
    print("-l --local - load an existing locally saved .graphml file")


def get_arg():
    args = sys.argv[1:]
    options = "hdl"
    long_options = ["help", "download", "local"]
    if not args:
        usage()
        return
    try:
        arguments, values = getopt.getopt(args, options, long_options)
        for currentArg, currentVal in arguments:
            if currentArg in ("-h", "--help"):
                print("Showing Help")
                usage()
            elif currentArg in ("-d", "--download"):
                print("downloading")
                download()
            elif currentArg in ("-l", "--local"):
                local()
            else:
                usage()
    except getopt.error as err:
        print(str(err))





def local():
    f = os.listdir()
    p = input("Enter the (full)file name of the .graphml file in the working directory ")
    if p in f:
        G = ox.io.load_graphml(filepath=p)
        interactive(G)
    else:
        print("The specified file is not present in the current directory")
    

def download():
    print("Enter the coordinates of the bounding box in decimals ")
    c1 = list(input("Enter the bottom-left coordinate(in decimal) using commas , ").split(","))
    c2 = list(input("Enter the top-right coordinate(in decimal) using commas , ").split(","))
    bbox = tuple([c1[1], c1[0], c2[1], c2[0]])
    
    print(c1,c2)

    print("Started fetching ...")
    G = ox.graph.graph_from_bbox(bbox, network_type='all', simplify=True, retain_all=True,truncate_by_edge=True, custom_filter=None)
    print("Done")

    ox.io.save_graphml(G, filepath="temp.graphml", gephi=True, encoding='utf-8')
    #ox.plot_figure_ground(G)
    interactive(G)

def interactive(G):
    fig, ax = ox.plot_graph(G, show=False, close=False, node_size=3)

    f = []
    def click(event):
        if event.inaxes == ax:
            x, y = event.xdata, event.ydata
            nn = ox.nearest_nodes(G, x ,y)
            print("Clicked on ",x," ",y)
            f.append(nn)

            ax.scatter(G.nodes[nn]["x"],G.nodes[nn]["y"],zorder = 20,c="red")
            fig.canvas.draw()
            if len(f) >= 2:
                fig.canvas.mpl_disconnect(cid)
                fig.canvas.new_timer(interval=3000,callbacks=[(plt.close, (fig,), {})]).start()


    cid = fig.canvas.mpl_connect("button_press_event",click)
    plt.show()
    orig, dest = f[0],f[1]
    route = ox.routing.shortest_path(G, orig, dest, weight='length', cpus=1)
    if route == None:
        print("It is not possible to select a route between those points")
    else:
        fig, ax = ox.plot.plot_graph_route(G, route,route_color='r', route_linewidth=4, route_alpha=0.5, orig_dest_size=100, ax=None, node_size=3)



def main():
    print("Welcome to the neighbourhood route finder terminal application ")
    get_arg()
    #G = ox.io.load_graphml(filepath="graph.graphml")
    #interactive(G)

main()