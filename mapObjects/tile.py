class tile:
    """
    A map tile. May or may not be blocked, may or may not be transparent.
    """

    def __init__(self, blocked, blockSight=None):
        self.blocked = blocked

        # Default: a blocked tile blocks sight
        if blockSight is None:
            blockSight = blocked

        self.blockSight = blockSight

        self.explored = False
        