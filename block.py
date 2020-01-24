class Block:
    
    '''
    fields=[
        'hash','confirmations','strippedsize','size','weight','height',
        'version','versionHex','merkleroot','tx','time','mediantime'
        'nonce','bits','difficulty','chainwork','nTx','previousblockhash'
        ]
    '''

    def __init__(self,response):
        """
        Initializatio of Block element.
        Function arguments:
                            response -> dictionary structure received from blockchain.oss.unist.hr with API getblock() function.

        """
        self.hash=response['hash'] if 'hash' in response else None
        self.confirmations=response['confirmations'] if 'confirmations' in response else None
        self.strippedsize=response['strippedsize'] if 'strippedsize' in response else None
        self.size=response['size'] if 'size' in response else None
        self.weight=response['weight'] if 'weight' in response else None
        self.height=response['height'] if 'height' in response else None
        self.version=response['version'] if 'version' in response else None
        self.versionHex=response['versionHex'] if 'versionHex' in response else None
        self.merkleroot=response['merkleroot'] if 'merkleroot' in response else None
        self.tx=response['tx'] if 'tx' in response else None
        self.time=response['time'] if 'time' in response else None
        self.mediantime=response['mediantime'] if 'mediantime' in response else None
        self.nonce=response['nonce'] if 'nonce' in response else None
        self.bits=response['bits'] if 'bits' in response else None
        self.difficulty=int(response['difficulty']) if 'difficulty' in response else None
        self.chainwork=response['chainwork'] if 'chainwork' in response else None
        self.nTx=response['nTx'] if 'nTx' in response else None
        self.previousblockhash=response['previousblockhash'] if 'previousblockhash' in response else None
        self.nextblockhash=response['nextblockhash'] if 'nextblockhash' in response else None
    
    def save(self,database):
        """
        Function saves block element to local database. Database file must be in same directory as script.
        Function argument:
                            database -> local database filename
        """
        # Saves one block in database and commits.
        with database: # Sends commit after execution.
            database.execute(
                "insert into block values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                None,
                self.hash,
                self.confirmations,
                self.strippedsize,
                self.size,
                self.weight,
                self.height,
                self.version,
                self.versionHex,
                self.merkleroot,
                str(self.tx),
                self.time,
                self.mediantime,
                self.nonce,
                self.bits,
                self.difficulty,
                self.chainwork,
                self.nTx,
                self.previousblockhash,
                self.nextblockhash)
                )
