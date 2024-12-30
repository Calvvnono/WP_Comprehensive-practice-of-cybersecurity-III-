import gmpy2
from Crypto.Util.number import *

# RSA参数
N1 = 27682578737141139764880192910976946263355689816882797515059917479242862799083599745594956880258244112867559722435850732812023189662581052511287867553308318268020022386306820424829898858029986193412922645944359409248568131057377380697236238480724883073062491532254626363468032145049953168789073328812076794158602028961853986034378144749656228541552641207393473830715156452473432130040360471566096165146087202836036783304640579183082301858529818598032339821237841219774124710789761912675044056265735587753304064079484844965820681168729776560497921764083742448045654891113500035063474318442078036531813957551086231747079155691690001433127187382636049871228279519466735719768798574776353687049667125384146566107739705553580693984918816215940308884007192621418304753551998125658993859095063641090798574130161651257890916914325076137436869018454577522833
c1 = 14360977893873474578201937159000122429359790977572665232657843468076201963407780015131857192621550737338805880514393357390576423731328871867241029260294051045710144482989801857054158816998897546124709802730198690244128545073634486145786763294634081834588146373913232490890078533918320777534358739106486350300547206365723045306767038214923412032633833255742963954701475401704385045019069883734625251436409851588044241336835452728962860280865504000103361559688861149086469939940113748174610019620309023214292662384279070127090992947332945432141695583191136521301940116585610033790348125114471980285332011918355578839128892075058698885319243593345096734776497817461251643381989958326810478500026684389358920342021836572511688796450072700142033952403561408907486022094802237175920044147084170050294965826258250618675638343726352907476393474128674488943
E1 = 138906518221471521524404330039616633297752765534176570868900039237133419857485415639423196636068397237296224442083213768630488100717977884415342104239280950424735129147986053115335928783190377695248250926374734988108972136349625965753649992146322810352768246041575396721661142246729747572832017510241749082431
N2 = 27682578737141139764880192910976946263355689816882797515059917479242862799083599745594956880258244112867559722435850732812023189662581052511287867553308576254232706953290519059976159239205559295965110148734449650209977235953163255494808056707188551192674128213090005439928085856216617642935948961573449294338310127166077195263402939848861686214485115686799032901147314759348481062418109120418661302585413868782602282463165171129063197961455779193665041902822948963032580054067050227612838335828201043413949164885293325493829570131849345344856137656453666135670724974184749115550720826497558763320127218251970576144750319782121194483563545371157323166968983176013145267856898865437101799958588342741257457472036311490402279982286349929050116350394664561659857216725849236910894778018502118673902399095646487808462155207034764432342699549109080808769
c2 = 11293777290569693972360166961981727494638218221438571150393361751316389824613571820229370915191500766619410597117671232443452691634734112652285521806824284959073558010661204730954928847260946403867297932862687770449632506087883187920107766050673462588812979708792790888354008526054467620780053118019643408427959406056087370960170992834047890080269663747877143270683069575318397144844481262382463469080755423097527007161449411933936669451476467352049264455203632729909164666006688294056405955940041007137719228484035343153943155100892867641033645111253109951972003798413524003505574000784399458705347262353155363413513341797868942085136977548116650815336000627353933708913237438841909324920070013498153627767891674969586034872104569344923832761239959420543717354211689339868787331074579605476477152218068810732089913023456240425720821047030224659918
E2 = 138906518221471521524404330039616633297752765534176570868900039237133419857485415639423196636068397237296224442083213768630488100717977884415342104239280950424735129147986053115335928783190377695248250926374734988108972136349625965753649992146322810352768246041575396721661142246729747572832017510241749082619

# 求出次进行辗转相除的ai, 连分数可以通过ai的形式表示出来如a0+1/[a1+/[...]], 所以求出ai是十分必要的
def continued_fraction(x, y):
    cf = []
    while y:
        cf.append(x // y)
        x, y = y, x % y
    return cf

# 将连分数简化为分子和分母
def simplify_fraction(cf):
    numerator = 0
    denominator = 1
    for x in cf[::-1]:
        numerator, denominator = denominator, x * denominator + numerator
    return numerator, denominator

# 获取所有渐进分数
def get_convergents(cf):
    convergents = []
    for i in range(1, len(cf)):
        convergents.append(simplify_fraction(cf[:i]))
    return convergents

# Wiener攻击
def wiener_attack(e, n):
    cf = continued_fraction(e, n)
    for k, d in get_convergents(cf):
        if d == 0:
            continue
        if N1 % d == 0 and d != 1:
            return d
    print('not find!')

# 主函数
def main():
    q1 = wiener_attack(N1, N2)
    p1 = gmpy2.iroot(N1 // q1, 2)[0]
    p2 = gmpy2.next_prime(p1)
    q2 = gmpy2.next_prime(q1)
    
    phi1 = p1 * (p1 - 1) * (q1 - 1)
    phi2 = p2 * (p2 - 1) * (q2 - 1)
    
    d1 = inverse(E1, phi1)
    d2 = inverse(E2, phi2)
    
    m1 = pow(c1, d1, N1)
    m2 = pow(c2, d2, N2)
    
    print(long_to_bytes(m1) + long_to_bytes(m2))

if __name__ == "__main__":
    main()