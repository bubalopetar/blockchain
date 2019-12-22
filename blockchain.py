from block import Block
from bitcoinrpc.authproxy import AuthServiceProxy
import sqlite3
import PySimpleGUI as sg


DATABASE='blockchain.db'
CLIENT_URL= 'http://student:WYVyF5DTERJASAiIiYGg4UkRH@blockchain.oss.unist.hr:8332'

def get_blocks(client,n=0):
    '''
    Function to retrieve block starting from genesis.
    Function arguments:
                        n -> number of blocks to save from genesis block.
    '''
    # Connect to database
    db=sqlite3.connect(DATABASE)

    # Firstly save genesis block
    block=Block(client.getblock(client.getblockhash(0)))
    block.save(db)

    # If only one element is selected.
    if n==1:
        db.close()
        return

    # If n is not selected, download whole blockchain
    if n==0:
        # Go through nexblockhash and save blocks
        while block.nextblockhash:
            block=Block(client.getblock(block.nextblockhash))
            block.save(db)
            sg.PopupAnimated('loading.gif')
        sg.PopupAnimated(None)
        db.close()

    # Download n of blocks.
    else:
        for i in range(n-1):
            block=Block(client.getblock(block.nextblockhash))
            block.save(db)
            sg.PopupAnimated('loading.gif')
        sg.PopupAnimated(None)
        db.close()
            

def get_last_n_blocks(client,n):
    """
    Function to retreive last n block from client node.
    Function arguments:
                        client -> client bitcoin node, e.g. ( blockchain.oss.unist.hr )
                        n      -> number of blocks to retrive
    """

    # Connect to local Database
    db=sqlite3.connect(DATABASE)


    # Get last block in blockchain
    block=Block(client.getblock(client.getbestblockhash()))
    block.save(db)

    # Save last n blocks
    for i in range(n):
            block=Block(client.getblock(block.previousblockhash))
            block.save(db)
            sg.PopupAnimated('loading.gif')
    sg.PopupAnimated(None)

    db.close()

def layout():
    '''
    Design of window layout. Returns layout variable
    '''

    sg.change_look_and_feel('Light Blue 6')

    layout = [  
            [sg.Text('Database:'), sg.Text(DATABASE)],
            [sg.Text('Client Node:'), sg.Text(CLIENT_URL)],
            [sg.Text('Number of blocks to download (enter 0 to download whole blockchain)'),
            sg.Spin([i for i in range(1,10^5)], initial_value=1,size=(10,1)),
            sg.Checkbox('From latest block')],
            [sg.Button('Download blocks!')] 
    ]

    return layout

def main():
    
    # Connect to blockchain.oss.unist.hr
    client=AuthServiceProxy(CLIENT_URL)

    # Create GUI window.
    window=sg.Window('Blockchain',layout(),icon='blockchain.ico',)

    while True:
        event, values = window.read()
        if event in (None,):	# if user closes window
            break

        if event == 'Download blocks!':
            # Retrive number of blocks from input
            n=int(values[0]) 

            # Start downloading from latest block
            if values[1]==True:
                get_last_n_blocks(client,n)
            
            # Start downloading from genesis block
            else:
                get_blocks(client,n)

    window.close()

if __name__=='__main__':
    main()