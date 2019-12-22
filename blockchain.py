import block
from bitcoinrpc.authproxy import AuthServiceProxy
import sqlite3

DATABASE='blockchain.db'
CLIENT_URL= 'http://student:WYVyF5DTERJASAiIiYGg4UkRH@blockchain.oss.unist.hr:8332'

def get_all_blocks(client):
    '''
    Function to retrieve block starting from genesis.
    '''

    db=sqlite3.connect(DATABASE)
    block=Block(client.getblock(client.getblockhash(1)))
    block.save(db)

    while block.nextblockhash:
        block=Block(client.getblock(block.nextblockhash))
        block.save(db)
            
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
    for i in range(10):
            block=Block(client.getblock(block.previousblockhash))
            block.save(db)

    db.close()

def get_n_blocks_from_start(client,n):
    """
    Function to retreive first n block from client node.
    Function arguments:
                        client -> client bitcoin node, e.g. ( blockchain.oss.unist.hr )
                        n      -> number of blocks to retrive
    """

    # Connect to local Database
    db=sqlite3.connect(DATABASE)

    # Get genesis block
    block=Block(client.getblock(client.getblockhash(0)))
    block.save(db)

    # Save last n blocks
    for i in range(n):
            block=Block(client.getblock(block.nextblockhash))
            block.save(db)

    db.close()

def main():
    
    # Connect to blockchain.oss.unist.hr
    client=AuthServiceProxy(CLIENT_URL)

    #get_last_n_blocks(client,10)
    #get_n_blocks_from_start(client,10)
    #get_all_blocks(client)
    
    #print(len(client.getblock(client.getbestblockhash(),2)['tx']))


if __name__=='__main__':
    main()