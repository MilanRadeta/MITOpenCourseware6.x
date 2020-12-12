## Factory Simulator

'''A factory makes parts. The parts go from machine to machine.
   Different part types have their own classes, and each class includes a last_id,
   counting how many of that type of part have been created.'''
class Part:
    last_id = 0
    def __init__(self):
        self.__class__.last_id += 1
        self.id = self.last_id

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.id})>"

class Nut(Part):
    last_id = 0

class Bolt(Part):
    last_id = 0

'''An assembly is a part that is a composition of multiple parts.'''
class Assembly(Part):
    last_id = 0
    def __init__(self, parts):
        super().__init__()
        self.sub = parts

    def __repr__(self):
        return f"<{self.__class__.__name__}({self.id}) {self.sub}>"


class Toy(Assembly):
    last_id = 0

class Shiny(Assembly):
    last_id = 0

'''Parts travel between machines on a conveyor belt.
   size == -1 means there is no size limit to the belt.'''
class ConveyorBelt():
    def __init__(self,  name, size):
        self.parts = []         # parts in the belt
        self.name = name
        self.size = size        # maximum capacity of the belt

    # add parts to the belt
    def push(self, parts):
        self.parts.append(parts)

    # get a part from the belt (if parts exist)
    def pop(self):
        return self.parts.pop(0) if len(self.parts) > 0 else None

    # see the part in a given position
    def peek(self, n):
        return self.parts[n] if self.parts and len(self.parts) > n else None

    # is there room in the belt to add a part?
    def has_space(self):
        return len(self.parts) < self.size if self.size > 0 else True

    def report(self):
        print(f"   {self.name}: {self.parts}")


    def __len__(self):
        return len(self.parts)

    def __repr__(self):
        return f"<{self.name:}{self.parts}>"


'''A machine operates by taking items from the input queue, working on them for some time,
   and producing an item that is put in the output queue.'''
class Machine:
    def __init__(self, in_queues, out_queue, time_required):
        self.tat = time_required    # time required to produce one new part
        self.in_queues = in_queues
        self.out_queue = out_queue

        self.state = 'waiting'      # status can be 'waiting' and 'busy'
        self.time_remaining = 0     # how much time is left to produce a part
        self.parts = []             # parts on the working list

    def timestep(self):
        # machine working on a part
        if self.state == 'busy':
            self.time_remaining -= 1                    # one time tick gone
            if self.time_remaining <= 0:
                self.finish_operation(self.out_queue)   # done that item
                self.state = 'waiting'
        elif self.state == 'waiting':
            # see if we can start working on the next item
            if self.start_operation(self.in_queues, self.out_queue):
                self.state = 'busy'
                self.time_remaining = self.tat

    # Start producing an item
    def start_operation(self, queues, out_queue):
        # has room to put the item in the output queue
        if not out_queue.has_space():
            return False
        # check all input queues have parts
        for q in queues:
            if q.peek(0) == None:
                return False
        # get parts and start producing
        for q in queues:
            self.parts = self.parts + [q.pop()]
        return True

    # done production
    def finish_operation(self, queue):
        for p in self.parts:        # put the parts back
            queue.push(p)
        self.parts = []

    def report(self):
        print(f"   {self.__class__.__name__}: {self.state} ({self.time_remaining} of {self.tat}) holding {self.parts}")

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.state} ({self.time_remaining} of {self.tat})>"


'''This is a factory where all the machines and conveyor belts live.
   It will simulate the operation by one time step at a time.'''
class Factory():
    def __init__(self, anime=None):
        self.anime = anime
        self.time = 0
        self.machines = []
        self.output_queue = ConveyorBelt("Finished Goods", -1)
        self.queues = [self.output_queue]


    def simulate(self, num_steps, report=False):
        if report: print("Starting simulation at time", self.time)
        while num_steps > 0:
            if report: self.report()
            # all the machines carry out a time step
            for m in self.machines:
                m.timestep()
            self.time += 1
            num_steps -= 1
            if self.anime:
                self.anime.run_epoh()
        if report: self.report()
        if report: print("Ending simulation at time", self.time)

    def report(self):
        print(" time:", self.time)
        for m in self.machines:
            m.report()
        for q in self.queues:
            q.report()
        if len(self.output_queue) > 0:
            print("  Last part out:", self.output_queue.peek(-1))


'''Paint the nuts!'''
class TinyFactory(Factory):
    def __init__(self, anime=None):
        super().__init__(anime)
        nuts = InfiniteSupply("nut supply", Nut)
        self.queues += [nuts]
        asm = Painter(nuts, self.output_queue)
        self.machines += [asm]

        if anime:
            anime.setup([nuts, asm, self.output_queue])
        
'''Get the nuts and bolts, assemble a toy, and paint it.'''
class ToyFactory(Factory):
    def __init__(self, anime=None):
        super().__init__(anime)
        nuts = InfiniteSupply("Nut supply", Nut)
        bolts = InfiniteSupply("Bolt supply", Bolt)
        nutqueue = ConveyorBelt("Nuts", 6)
        boltqueue = ConveyorBelt("Bolts", 2)
        toyqueue = ConveyorBelt("Toys", 4)

        nutloader = Loader(nuts, nutqueue)
        boltloader = Loader(bolts, boltqueue)
        assembler = Assembler(nutqueue, boltqueue, toyqueue)
        painter = Painter(toyqueue, self.output_queue)

        self.queues += [nuts, bolts, nutqueue, boltqueue, toyqueue]
        self.machines += [nutloader, boltloader, assembler, painter]

        if anime:
            anime.setup([[nuts, bolts],[nutloader, boltloader], [nutqueue, boltqueue], assembler, toyqueue, painter, self.output_queue])

class Anime():
    def setup(self, mylist):
        self.mylist = mylist

    def run_epoch(self):
        pass

def runTinyFactory(anime=None):
    tf = TinyFactory(anime)
    for i in range(5):
        tf.simulate(20, report=anime is None)

def runToyFactory(anime=None):
    tf = ToyFactory(anime)
    for i in range(5):
        tf.simulate(20, report=anime is None)
