class Parser:
    def __init__(self):
        self.token_buffer = []

    def tokenize(self, s):
        (s0, string_dic) = self.parse_string(s)
        s1 = s0.replace('(', ' ( ')
        s2 = s1.replace(')', ' ) ')
        s3 = s2.replace('\'', ' \' ')
        tokens = s3.split()
        self.do_quote(tokens, 0)
        for key in string_dic.keys():
            if key in tokens:
                index = tokens.index(key)
                tokens[index] = string_dic[key]
        return tokens

    def parse_string(self, s):
        string_dic = {}
        i = 0
        string_no = 0
        string_start = 0
        string_mark = False
        while i < len(s):
            ch = s[i]
            if ch == '"':
                if string_mark:
                    string_mark = False
                    string_end = i + 1
                    string_body = s[string_start:string_end]
                    s = s.replace(string_body, '_s%d' % string_no, 1)
                    string_dic['_s%d' % string_no] = string_body[1:len(string_body)-1]
                    string_no = string_no + 1
                    i = i - (len(string_body) + 2) + 3
                else:
                    string_mark = True
                    string_start = i
            i = i + 1
        return s, string_dic

    def do_quote(self, tokens, index):
        while index < len(tokens):
            token = tokens[index]
            if token == '\'':
                tokens[index] = '('
                index = index + 1
                tokens.insert(index, 'quote')
                index = index + 1
                index = self.add_quote(tokens, index)
                tokens.insert(index, ')')
                index = index + 1
            else:
                index = index + 1
        return index

    def add_quote(self, tokens, index):
        if not tokens[index] in ['(', ')', '\'']:
            return index + 1
        paren_cnt = 0
        while index < len(tokens):
            token = tokens[index]
            if token == '(':
                paren_cnt = paren_cnt + 1
            elif token == ')':
                paren_cnt = paren_cnt - 1
                if paren_cnt == 0:
                    return index
            elif token == '\'':
                index = self.do_quote(tokens, index)
            index = index + 1
        return index

    def parse_token_paren(self, tokens):
        i = 0
        last_index = 0
        paren_level = 0
        s_list = []
        while i < len(tokens):
            if tokens[i] == '(':
                paren_level = paren_level + 1
            elif tokens[i] == ')':
                paren_level = paren_level - 1
                if paren_level == 0:
                    paren_closed_tokens = tokens[last_index: i + 1]
                    s_list.append(paren_closed_tokens)
                    last_index = i + 1
            elif paren_level == 0:
                s_list.append([tokens[i]])
                last_index = i + 1
            i = i + 1

        if last_index == len(tokens):
            tokens.clear()
        elif last_index != 0:
            del tokens[:last_index]
        return s_list

    def parse_text(self, t):
        tokens = self.tokenize(t)
        self.token_buffer.extend(tokens)
        s_exps = self.parse_token_paren(self.token_buffer)
        return s_exps
