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
            sg.PopupAnimated('./graphic/loading.gif')
        sg.PopupAnimated(None)
        db.close()

    # Download n of blocks.
    else:
        for i in range(n-1):
            block=Block(client.getblock(block.nextblockhash))
            block.save(db)
            sg.PopupAnimated('./graphic/loading.gif')
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

    # Get last - n block in blockchain starting from n to end
    block=Block(client.getblock( client.getblockhash( client.getblockcount()-n ) ))
    block.save(db)

    # Save last n blocks
    for i in range(n):
            block=Block(client.getblock(block.nextblockhash))
            block.save(db)
            sg.PopupAnimated('./graphic/loading.gif')
    sg.PopupAnimated(None)

    db.close()

def read_blocks_from_database():
    """
    Read blocks from database.
    Returns array of blocks.
    """
    # Connect to database
    db=sqlite3.connect(DATABASE)

    # Get all data and column names
    data=db.execute('select * from block')
    data=data.fetchall()
    columns=[
        'ID','hash','confirmations','strippedsize','size','weight','height',
        'version','versionHex','merkleroot','tx','time','mediantime',
        'nonce','bits','difficulty','chainwork','nTx','previousblockhash','nextblockhash'
        ]
    return data,columns

def delete_blocks():
    '''
    Clears blocks table.
    '''

    # Connect to database
    db=sqlite3.connect(DATABASE)
    with db:
        db.execute('DELETE FROM block')
    db.close()

    return True


def layout():
    '''
    Design of window layout. Returns layout variable
    '''

    sg.change_look_and_feel('Light Blue 6')

    # Download tab
    tab1=  [
            [
                sg.T(' ')
            ],
            [
                sg.Frame('Info',layout=[
                        [sg.Text('Database:   '), sg.InputText(default_text=DATABASE,enable_events=True,key='Database',size=(500,1))],
                        [sg.Text('Client Node:'),sg.InputText(default_text=CLIENT_URL,enable_events=True,key='Client Node',size=(500,1))]
                        ]
                    )
            ],
            [
                sg.T(' ')
            ],
            [
                sg.Text('Number of blocks to download (enter 0 to download whole blockchain)'),
                sg.Spin([i for i in range(1,10^5)], initial_value=1,size=(10,1))
            ],
            [
                sg.Checkbox('Download last n blocks'),sg.Button('Download blocks!')
            ]
        
    ]

    data,columns=read_blocks_from_database()
    # If there is no data in database
    if len(data)==0:
        data=[[' ' for i in range(len(columns))]]

    # Database tab
    tab2= [
        
        [sg.Table(values=data,headings= columns,key='table',num_rows=7,vertical_scroll_only=False)],
        [sg.Button('Empty Database',size=(1000,1))]
        
    ]    

    # General layout
    layout = [[sg.TabGroup([[sg.Tab('Download', tab1, tooltip='tip',key='tab1'), sg.Tab('Database',tab2,key='tab2')]], tooltip='TIP2')]]  

    return layout

def main():

    global CLIENT_URL
    global DATABASE
    
    # Connect to blockchain.oss.unist.hr
    client=AuthServiceProxy(CLIENT_URL)

    # Create GUI window.
    window=sg.Window('Blockchain',layout(),icon='./graphic/blockchain.ico',resizable=True,size=(660,250))

    while True:
        event, values = window.read()
        if event in (None,):	# if user closes window
            break

        if event == 'Download blocks!':
            # Retrive number of blocks from input
            n=int(values[0]) 

            # Download last n blocks
            if values[1]==True:
                get_last_n_blocks(client,n)
                window.FindElement('table').Update(values=read_blocks_from_database()[0])
            
            # Start downloading from genesis block
            else:
                get_blocks(client,n)
                window.FindElement('table').Update(values=read_blocks_from_database()[0])

        elif event == 'Empty Database':
            delete_blocks()
            window.FindElement('table').Update(values=read_blocks_from_database()[0])
        
        elif event=="Client Node":
            CLIENT_URL=values['Client Node'].strip()
        
        elif event=="Database":
            DATABASE=values['Database'].strip()

    window.close()
    
if __name__=='__main__':
    main()