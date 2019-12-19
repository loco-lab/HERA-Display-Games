import numpy as np

led_map = {
    [0,0]:10,
    [1,0]:9,
    [2,0]:8,
    [3,0]:7,
    [4,0]:6,
    [5,0]:5,
    [6,0]:4,
    [7,0]:3,
    [8,0]:2,
    [9,0]:1,
    [10,0]:0,
    [11,0]:'dead',

    [0,1]:11,
    [1,1]:12,
    [2,1]:13,
    [3,1]:14,
    [4,1]:15,
    [5,1]:16,
    [6,1]:17,
    [7,1]:18,
    [8,1]:19,
    [9,1]:20,
    [10,1]:21,
    [11,1]:'dead',
    [12,1]:119,

    [0,2]:32,
    [1,2]:31,
    [2,2]:30,
    [3,2]:29,
    [4,2]:28,
    [5,2]:27,
    [6,2]:26,
    [7,2]:25,
    [8,2]:24,
    [9,2]:23,
    [10,2]:22,
    [11,2]:'dead',
    [12,2]:118,
    [13,2]:120,

    [0,3]:33,
    [1,3]:34,
    [2,3]:35,
    [3,3]:36,
    [4,3]:37,
    [5,3]:38,
    [6,3]:39,
    [7,3]:40,
    [8,3]:41,
    [9,3]:42,
    [10,3]:43,
    [11,3]:'dead',
    [12,3]:117,
    [13,3]:121,
    [14,3]:139,

    [0,4]:54,
    [1,4]:53,
    [2,4]:52,
    [3,4]:51,
    [4,4]:50,
    [5,4]:49,
    [6,4]:48,
    [7,4]:47,
    [8,4]:46,
    [9,4]:45,
    [10,4]:44,
    [11,4]:'dead',
    [12,4]:116,
    [13,4]:122,
    [14,4]:138,
    [15,4]:140,

    [0,5]:55,
    [1,5]:56,
    [2,5]:57,
    [3,5]:58,
    [4,5]:59,
    [5,5]:60,
    [6,5]:61,
    [7,5]:62,
    [8,5]:63,
    [9,5]:64,
    [10,5]:65,
    [11,5]:'dead',
    [12,5]:115,
    [13,5]:123,
    [14,5]:137,
    [15,5]:141,
    [16,5]:159,

    [0,6]:76,
    [1,6]:75,
    [2,6]:74,
    [3,6]:73,
    [4,6]:72,
    [5,6]:71,
    [6,6]:70,
    [7,6]:69,
    [8,6]:68,
    [9,6]:67,
    [10,6]:66,
    [11,6]:'dead',
    [12,6]:114,
    [13,6]:124,
    [14,6]:136,
    [15,6]:142,
    [16,6]:158,
    [17,6]:160,

    [0,7]:77,
    [1,7]:78,
    [2,7]:79,
    [3,7]:80,
    [4,7]:81,
    [5,7]:82,
    [6,7]:83,
    [7,7]:84,
    [8,7]:85,
    [9,7]:86,
    [10,7]:87,
    [11,7]:'dead',
    [12,7]:113,
    [13,7]:125,
    [14,7]:135,
    [15,7]:143,
    [16,7]:157,
    [17,7]:161,
    [18,7]:179,

    [0,8]:98,
    [1,8]:97,
    [2,8]:96,
    [3,8]:95,
    [4,8]:94,
    [5,8]:93,
    [6,8]:92,
    [7,8]:91,
    [8,8]:90,
    [9,8]:89,
    [10,8]:88,
    [11,8]:'dead',
    [12,8]:112,
    [13,8]:126,
    [14,8]:134,
    [15,8]:144,
    [16,8]:156,
    [17,8]:162,
    [18,8]:178,
    [19,8]:180,

    [0,9]:99,
    [1,9]:100,
    [2,9]:101,
    [3,9]:102,
    [4,9]:103,
    [5,9]:104,
    [6,9]:105,
    [7,9]:106,
    [8,9]:107,
    [9,9]:108,
    [10,9]:109,
    [11,9]:'dead',
    [12,9]:111,
    [13,9]:127,
    [14,9]:133,
    [15,9]:145,
    [16,9]:155,
    [17,9]:163,
    [18,9]:177,
    [19,9]:181,
    [20,9]:199,

    [0,10]:'dead',
    [1,10]:'dead',
    [2,10]:'dead',
    [3,10]:'dead',
    [4,10]:'dead',
    [5,10]:'dead',
    [6,10]:'dead',
    [7,10]:'dead',
    [8,10]:'dead',
    [9,10]:'dead',
    [10,10]:'dead',
    [11,10]:'dead',
    [12,10]:110,
    [13,10]:128,
    [14,10]:132,
    [15,10]:146,
    [16,10]:154,
    [17,10]:164,
    [18,10]:176,
    [19,10]:182,
    [20,10]:198,
    [21,10]:200,

    [1,11]:309,
    [2,11]:310,
    [3,11]:311,
    [4,11]:312,
    [5,11]:313,
    [6,11]:314,
    [7,11]:315,
    [8,11]:316,
    [9,11]:317,
    [10,11]:318,
    [11,11]:319,
    [12,11]:'dead',
    [13,11]:129,
    [14,11]:131,
    [15,11]:147,
    [16,11]:153,
    [17,11]:165,
    [18,11]:175,
    [19,11]:183,
    [20,11]:197,
    [21,11]:201,

    [2,12]:308,
    [3,12]:307,
    [4,12]:306,
    [5,12]:305,
    [6,12]:304,
    [7,12]:303,
    [8,12]:302,
    [9,12]:301,
    [10,12]:300,
    [11,12]:299,
    [12,12]:298,
    [13,12]:'dead',
    [14,12]:130,
    [15,12]:148,
    [16,12]:152,
    [17,12]:166,
    [18,12]:174,
    [19,12]:184,
    [20,12]:196,
    [21,12]:202,

    [3,13]:287,
    [4,13]:288,
    [5,13]:289,
    [6,13]:290,
    [7,13]:291,
    [8,13]:292,
    [9,13]:293,
    [10,13]:294,
    [11,13]:295,
    [12,13]:296,
    [13,13]:297,
    [14,13]:'dead',
    [15,13]:149,
    [16,13]:151,
    [17,13]:167,
    [18,13]:173,
    [19,13]:185,
    [20,13]:195,
    [21,13]:203,

    [4,14]:286,
    [5,14]:285,
    [6,14]:284,
    [7,14]:283,
    [8,14]:282,
    [9,14]:281,
    [10,14]:280,
    [11,14]:279,
    [12,14]:278,
    [13,14]:277,
    [14,14]:276,
    [15,14]:'dead',
    [16,14]:150,
    [17,14]:168,
    [18,14]:172,
    [19,14]:186,
    [20,14]:194,
    [21,14]:204,

    [5,15]:265,
    [6,15]:266,
    [7,15]:267,
    [8,15]:268,
    [9,15]:269,
    [10,15]:270,
    [11,15]:271,
    [12,15]:272,
    [13,15]:273,
    [14,15]:274,
    [15,15]:275,
    [16,15]:'dead',
    [17,15]:169,
    [18,15]:171,
    [19,15]:187,
    [20,15]:193,
    [21,15]:205,

    [6,16]:264,
    [7,16]:263,
    [8,16]:262,
    [9,16]:261,
    [10,16]:260,
    [11,16]:259,
    [12,16]:258,
    [13,16]:257,
    [14,16]:256,
    [15,16]:255,
    [16,16]:254,
    [17,16]:'dead',
    [18,16]:170,
    [19,16]:188,
    [20,16]:192,
    [21,16]:206,

    [7,17]:243,
    [8,17]:244,
    [9,17]:245,
    [10,17]:246,
    [11,17]:247,
    [12,17]:248,
    [13,17]:249,
    [14,17]:250,
    [15,17]:251,
    [16,17]:252,
    [17,17]:253,
    [18,17]:'dead',
    [19,17]:189,
    [20,17]:191,
    [21,17]:207,

    [8,18]:242,
    [9,18]:241,
    [10,18]:240,
    [11,18]:239,
    [12,18]:238,
    [13,18]:237,
    [14,18]:236,
    [15,18]:235,
    [16,18]:234,
    [17,18]:233,
    [18,18]:232,
    [19,18]:'dead',
    [20,18]:190,
    [21,18]:208,

    [9,19]:221,
    [10,19]:222,
    [11,19]:223,
    [12,19]:224,
    [13,19]:225,
    [14,19]:226,
    [15,19]:227,
    [16,19]:228,
    [17,19]:229,
    [18,19]:230,
    [19,19]:231,
    [20,19]:'dead',
    [21,19]:209,

    [10,20]:220,
    [11,20]:219,
    [12,20]:218,
    [13,20]:217,
    [14,20]:216,
    [15,20]:215,
    [16,20]:214,
    [17,20]:213,
    [18,20]:212,
    [19,20]:211,
    [20,20]:210,
    [21,20]:'dead',


}













