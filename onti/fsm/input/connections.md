|#|State|Signal|Next state|Action|
|:---:|:---:|:---:|:---:|:---:|
|1|s_star|this_is_true|s_0|empty|
|2|s_0|y_0|s_1__j|a_6__j|
|3|s_0|y_0__prime and y_17__i|t_1__i|b_18__i|
|4|s_0|y_0__prime and y_18__i|t_4__i|b_18__i|
|5|s_0|y_0__prime and y_19__i|t_6__i|b_18__i|
|6|s_0|y_0__prime and y_20__i|t_9__i|b_18__i|
|7|s_1__j|y_1__j|s_2__j|a_1__j|
|8|s_2__j|this_is_true|s_3__j|a_2__j|
|9|s_1__j|y_2__j|s_3__j|a_2__j|
|10|s_1__j|y_3__j and y_5__j and y_6 and y_7__j|s_3__j|a_3__j|
|11|s_1__j|y_4__j|s_0|a_0__j|
|12|s_1__j|y_3__j and not y_5__j|s_3__j|a_2__j|
|13|s_1__j|y_3__j and y_5__j and not y_6|s_3__j|a_4__j|
|14|s_1__j|y_3__j and y_5__j and y_6 and not y_7__j|s_3__j|a_5__j|
|15|s_3__j|this_is_true|s_0|a_0__j|
|16|t_1__i|y_14__i and y_8__i and not y_9__i|t_2__i|b_1__i|
|17|t_1__i|y_14__i and y_8__i and y_9__i|t_2__i|b_2__i|
|18|t_1__i|not y_14__i and y_8__i and not y_9__i|t_2__i|b_7__i|
|19|t_1__i|not y_14__i and y_8__i and y_9__i|t_2__i|b_8__i|
|20|t_1__i|y_14__i and y_10__i and not y_9__i|t_3__i|b_4__i|
|21|t_1__i|y_14__i and y_10__i and y_9__i|t_2__i|b_3__i|
|22|t_1__i|not y_14__i and (y_10__i or y_11__i or y_12__i or y_13__i)|t_2__i|b_8__i|
|23|t_1__i|y_14__i and y_13__i|t_2__i|b_2__i|
|24|t_1__i|y_14__i and y_11__i and y_9__i|t_8__i|b_9__i|
|25|t_1__i|y_14__i and y_11__i and not y_9__i|t_2__i|b_2__i|
|26|t_1__i|y_14__i and y_12__i|t_2__i|b_13__i|
|27|t_2__i|this_is_true|s_0|b_0__i|
|28|t_3__i|this_is_true|t_2__i|b_14__i|
|29|t_4__i|y_14__i and y_9__i|t_11__i|b_3__i|
|30|t_4__i|y_14__i and (y_8__i or y_10__i or y_11__i or y_12__i) and not y_9__i|t_2__i|b_4__i|
|31|t_4__i|y_14__i and y_13__i and not y_9__i|t_5__i|b_5__i|
|32|t_4__i|not y_14__i|t_11__i|b_8__i|
|33|t_5__i|this_is_true|t_2__i|b_15__i|
|34|t_6__i|y_14__i and y_9__i|t_11__i|b_3__i|
|35|t_6__i|y_14__i and (y_8__i or y_10__i or y_11__i or y_12__i) and not y_9__i|t_2__i|b_5__i|
|36|t_6__i|y_14__i and y_13__i and not y_9__i|t_7__i|b_6__i|
|37|t_6__i|not y_14__i|t_11__i|b_8__i|
|38|t_7__i|this_is_true|t_11__i|b_3__i|
|39|t_8__i|this_is_true|t_2__i|b_16__i|
|40|t_9__i|not y_9__i and y_14__i|t_11__i|b_2__i|
|41|t_9__i|not y_9__i and not y_14__i|t_11__i|b_8__i|
|42|t_9__i|y_9__i and (y_8__i or y_10__i or y_11__i or y_12__i)|t_2__i|b_10__i|
|43|t_9__i|y_9__i and y_13__i and not y_15__i and not y_16__i|t_2__i|b_10__i|
|44|t_9__i|y_9__i and y_15__i|t_10__i|b_12__i|
|45|t_9__i|y_9__i and y_16__i|t_11__i|b_11__i|
|46|t_10__i|this_is_true|t_11__i|b_1__i|
|47|t_11__i|this_is_true|t_2__i|b_17__i|
|48|s_0|y_99|s_star|a_99|
