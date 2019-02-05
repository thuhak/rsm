##author: thuhak.zhou@nio.com
import logging
from random import choices


class CheckState(type):
    def __init__(cls, clsname, bases, clsdict):
        super().__init__(clsname, bases, clsdict)
        sm = clsdict.get('state_info')
        valid_state = {x for x in clsdict.keys() if not x.startswith('_') and callable(clsdict[x])}
        valid_state.update({'entry', 'complete'})
        for s in sm:
            states = set(sm[s].keys())
            states.add(s)
            for st in states:
                if st not in valid_state:
                    raise ValueError('state {} is not valid method'.format(st))
            pos = sum(sm[s].values())
            if pos != 1:
                raise ValueError('sum of possibility must equals 1')


class RSM(metaclass=CheckState):
    '''
    random state machine
    '''
    state_info = {'entry': {'complete': 1.0}}

    def __init__(self):
        self.current_state = 'entry'

    def run(self):
        while self.current_state and self.current_state != 'complete':
            state_info = self.state_info.get(self.current_state, {})
            if not state_info:
                logging.info('can not find next state for {}'.format(self.current_state))
                break
            next_states = list(state_info.keys())
            weights = list(state_info.values())
            self.current_state = choices(next_states, weights, k=1)[0]
            state = getattr(self, self.current_state, None)
            if state:
                try:
                    logging.debug('start {}'.format(self.current_state))
                    state()
                except Exception as e:
                    logging.error('error in {}, error is {}'.format(self.current_state, str(e)))
                    break
