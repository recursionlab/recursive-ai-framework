Towards third generation HOTT
 Part 1: Basic syntax
 Michael Shulman
 University of San Diego
 joint work with Thorsten Altenkirch and Ambrus Kaposi
 CMU HoTT Seminar
 April 28, 2022
Outline
 1 Background
 2 Identity types
 3 Function extensionality
 4 Univalence
 5 From univalence to homotopy theory
First generation: Book HoTT
 Cf. AwodeyWarren, Voevodsky, The HoTT Book
 1 Based on Intensional Martin-Lof Type Theory
 2 Identity types characterized by path induction
 3 Univalence is an axiom
 Advantages:
 Easy to do in Coq/Agda: assume univalence and away you go.
 Has models in all higher toposes.
 Disadvantages:
 Not computational (UA axiom is stuck)
 Many laws are not de nitional:
 IdA B((ab) (a b)) IdA(aa) IdB(bb)
 apf g(p) apf(apg(p))
 tr x A(x) B(x)(p (ab)) (trA(pa) trB(pb))
Second generation: Cubical type theories
 Cf. Bezem-Coquand-Huber, Cohen-Coquand-Huber-Mortberg,
 Angiuli-Brunerie-Coquand-Favonia-Harper-Licata
 1 Paths de ned as maps out of an interval exo-type I
 2 Cubical Kan operations asserted explicitly in syntax
 3 Univalence proved from glue types
 Advantages:
 Satis es canonicity and normalization
 Many equalities become de nitional
 Implemented in Cubical Agda, cooltt, ...
 Disadvantages:
 Not yet known to have models in higher toposes...
 . . . but it probably does (cf. ACCRS, cubical model for spaces).
 . . . ?
Whats not to like about cubical type theories?
 Martin-Lof J-elim is conceptually fundamental to equality . In
 Book HoTT, this simple rule automatically yields higher structure.
 Slogan for Book HoTT
 Homotopy is implicitly present in the foundations of mathematics.
 A nice story to tell philosophers.
 Accessible to students.
 In cubical type theory, identity is de ned using a homotopy-theoretic
 idea (paths), and higher structure is put in by hand (Kan ops).
 Fine if you already know you want to do homotopy theory.
 Doesnt have the same philosophical import.
 Not as accessible to students.
That interval
 The interval I is not an ordinary type, but appears in contexts.
 Complicates the meta-theory
 Harder to explain
 Harder to implement
 Termination-checking of boundaries
 Display of boundaries to the user
 Higher-order uni cation
 Were still learning how to implement cubical type theories.
 But its also worth exploring di erent approaches.
A problem shared by Book HoTT and CTT
 Chapter 2 of the Book characterizes lots of identity types:
 IdA B((ab) (a b)) IdA(aa) IdB(bb)
 IdA B(f g) 
(x:A)IdB(f (x) g(x))
 IdU(AB) Equiv(AB)
 In Book HoTT, these are all only equivalences.
 In cubical type theory, most of them are isomorphisms...
 . . . except for IdU, which is still only an equivalence!
 This limits the everyday usability of univalence. Given an
 equivalence f : A 
B : g, if we pass it through univalence we cant
 recover f or g de nitionally, only up to homotopy.
Towards H.O.T.T.
 I will describe work in progress towards a theory called
 Higher Observational Type Theory
 with the following properties:
 It admits models in all higher toposes, including spaces.
 Univalence by de nition (+ other Id characterizations).
 Homotopy theory is emergent rather than explicit;
 all rules have a convincing philosophical justi cation.
 Computation is a reasonable hope (no obvious stuck terms).
 Plan for the three talks:
 1 Basic syntax of H.O.T.T.
 2 Symmetries and semicartesian cubes
 3 Semantics of univalent universes
Outline
 1 Background
 2 Identity types
 3 Function extensionality
 4 Univalence
 5 From univalence to homotopy theory
Bishops conception of set
 Errett Bishop wrote that
 A set is de ned by describing exactly what must be done
 in order to construct an element of the set and what must
 be done in order to show that two elements are equal.
 MLTT follows this principle if equal refers to de nitional equality,
 giving introduction and rules:
 a : A
 b : B
 (ab) : A B
 1s 
1t : A
 2s 
2t : B
 s 
t : A B
 The elimination and rules are determined by harmony with the
 introduction rules.
Lower Observational Type Theory
 (Lower) Observational Type Theory (Altenkirch-McBride) applies
 the same principle to propositional equality types Eq.
 a : A
 b : B
 (ab) : A B
 p : EqA( 1s 1t)
 q : EqB( 2s 2t)
 (p =q) : EqA B(s t)
 But this theory is non-univalent by construction, with primitive UIP:
 p : EqA(x y)
 q : EqA(x y)
 irr(pq) : EqEqA(xy)(pq) 
Can we formulate a univalent version?
Notation and terminology
 In a univalent context, we refer to identity types, with formation rule
 A : U a:A b:A
 IdA(ab) : U
 The elements of an identity type are identi cations.
 Green highlights indicate rules of H.O.T.T.
 We omit unchanging ambient contexts .
Computing identity types
 The OTT rule
 p : EqA( 1s 1t)
 q : EqB( 2s 2t)
 (p =q) : EqA B(s t)
 says that EqA B behaves like EqA EqB. In a higher context, this
 would require in nitely many such rules for IdIdA B
 , etc. Instead, we
 make it a computation rule:
 IdA B(s t) IdA( 1s 1t) IdB( 2s 2t)
 Then we can just apply the same rule multiple times:
 IdIdA B(st)(pq) IdIdA( 1s 1t) IdB( 2s 2t)(pq)
 IdIdA( 1s 1t)( 1p 1q) IdIdB( 2s 2t)( 2p 2q)
Respect for equality
 Heres Bishop again (paraphrased):
 An operation f from A into B is called a function if we
 have f (a) = f(a) whenever aa A and a = a.
 For de nitional equality, MLTT has congruence rules for each
 primitive term former:
 s 
t : A B
 1s 
1t : A
 2s 
2t : B
 Lower OTT similarly asserts congruence terms:
 p : EqA B(s t)
 =
 1p : EqA( 1s 1t)
 =
 2p : EqB( 2s 2t)
 By structural induction, all terms respect both equalities.
Respect for higher equality
 We instead assert a general congruence term:
 x : A f :B p: IdA(aa)
 apxf (p) : IdB(f [a x] f [a x])
 In apxf (p), the variable x is bound in the term f .
 (For now, B doesnt depend on A; well come back to that later.)
 We give it computation rules on standard term-formers:
 apx(ab)(p) (apxa(p) apxb(p))
 apx 1s(p) 
1 apxs(p)
 apx 2s(p) 
2 apxs(p)
 These are well-typed by the previous rule IdA B IdA IdB.
 And for higher equalities, we can apply them multiple times.
Re exivity
 Everything is the same as itself, de nitionally and observationally:
 a : A
 a a:A
 Similarly, we assert re exivity terms:
 a : A
 a : EqA(aa)
 a : A
 re a : IdA(aa)
 with computation rules on standard term-formers:
 re (ab) 
(re a re b)
 re
 1s 
1re s
 re
 2s 
2re s
 Again, these rules are well-typed because IdA B IdA IdB.
ap on neutrals and redexes
 Note that apxf(p) computes on all terms that f could be, even
 those not headed by a constructor. The rules are consistent with
 computations occurring inside f ; for instance,
 apx 1(ab)(p) 
1 apx(ab)(p) 
1 (apxa(p) apxb(p)) apxa(p)
 can also be obtained by reducing 1(ab) a in the bound term.
 We complete the picture with rules for variables:
 apxx(p) p
 apxy(p) re y (if y is a variable= x)
 Then an ap term is never a normal form: it can always reduce.
 Think of it as a higher-dimensional explicit substitution f p x .
 modulo some detail well come back to later...
Functorial laws for ap
 Since ap always reduces, we can deduce by induction on terms the
 following admissible equalities:
 apxf (re a) re f[a x]
 apyg(apxf (p)) apxg[f y](p)
 apxt(p) re t (if x does not appear in t)
Outline
 1 Background
 2 Identity types
 3 Function extensionality
 4 Univalence
 5 From univalence to homotopy theory
Towards identity of functions
 The obvious rule for equality of functions is function extensionality:
 IdB C(f g) 
(y:B)IdC(f (y) g(y)) ?
 But this is trouble for ap on application. Given x : A f : B C
 and x : A b:B while p : IdA(aa), we want to compute
 apxfb(p) : IdC((f b)[a x] (f b)[a x])
 IdC(f [a x](b[a x]) f [a x](b[a x]))
 to something involving
 apxf (p) : IdB C(f[a x] g[a x])
 (y:B)IdC(f [a x](y) f [a x](y)) ?
 and
 apxb(p) : IdB(b[a x] b[a x])
 We need an equality in C between f[a x] and f[a x] applied to
 di erent inputs b[a x] and b[a x], but this apxf (p) cant give that.
Identity of functions
 A better rule is (still ignoring dependence of B on A)
 IdB C(f g) 
(u:B) (v:B) (q:IdB(uv))IdC(f (u) g(v))
 Once we have singleton contractibility, this will be equivalent to the
 nave version. But it also gives us
 apxf (p) : (u:B) (v:B) (q:IdB(uv))IdC(f [a x](u) f [a x](v))
 apxb(p) : IdB(b[a x] b[a x])
 so we can compute
 apxfb(p) : IdC(f [a x](b[a x]) f [a x](b[a x]))
 apxfb(p) apxf(p) b[a x] b[a x] apxb(p)
Identity of abstractions
 Let x : Ay : B t :C, hence x :A yt :B C. Given
 p : IdA(a0 a1), we can form apx( yt)(p), which has type
 IdB C(( yt)[a0 x] ( yt)[a1 x])
 (u:B) (v:B) (q:IdB(uv))IdC(t[a0 x u y] t[a1 x v y])
 How do we compute this?
Identity of abstractions
 Let x : Ay : B t :C, hence x :A yt :B C. Given
 p : IdA(a0 a1), we can form apx( yt)(p), which has type
 IdB C(( yt)[a0 x] ( yt)[a1 x])
 (u:B) (v:B) (q:IdB(uv))IdC(t[a0 x u y] t[a1 x v y])
 How do we compute this? We want to ap the term t on both p
 and q simultaneously. So we introduce a multi-variable ap:
 x1 : A1
 p1 : IdA1
 (a1 b1)
 xn : An t :C
 pn : IdAn
 (an bn)
 apx1 xnt(p1
 apx( yt)(p) 
pn) : IdC(t[a] t[b ])
 u v qapxyt(pq)
 (Still ignoring dependence in A1
 AnC.)
Computing with multi-variable ap
 Multi-variable ap computes with all the same rules we had before.
 The variable rules are
 apx1 xnxi
 (p1
 pn) pi
 apx1 xny(p1
 pn) re y (if y is a variable 
x1
 In addition, we can identify re exivity with the 0-ary ap
 (no bound variables in the subscript):
 re a 
ap()a()
 xn )
 Then all the computation rules for re become special cases of
 those for n-ary ap.
Outline
 1 Background
 2 Identity types
 3 Function extensionality
 4 Univalence
 5 From univalence to homotopy theory
Towards de nitional univalence
 We want univalence to hold by de nition , meaning IdU(AB)
 consists of equivalences. But what is an equivalence?
 Chapter 4 of the Book discusses several possibilites:
 1 Maps with contractible bers (Voevodsky equivalences)
 2 Half-adjoint equivalences
 3 Bi-invertible maps
 But philosophically, these all have problems:
 None feels canonical : why choose one over another?
 None is (de nitionally) symmetrical in A and B.
 Some are hard to motivate without homotopy theory a priori.
What is de nitional univalence?
 The HoTT Book gave three properties of a type Equiv(AB) to be
 a good notion of equivalence :
 1 There is an embedding Equiv(AB) , (A B).
 2 QInv(AB) Equiv(AB) over A B.
 3 Equiv(AB) QInv(AB) over A B.
 Here QInv(AB) is the nave type of quasi-invertible maps :
 QInv(AB) 
(f :A B) (g:B A) Id(g f 1A) Id(f g 1B)
 Univalence ( idtoeqv : IdU(AB) 
Equiv(AB) is an equivalence )
 can be stated equivalently using any such Equiv (but not QInv).
 can be stated equivalently using any such Equiv (but not QInv).
What is de nitional univalence?
 The HoTT Book gave three properties of a type Equiv(AB) to be
 a good notion of equivalence :
 1 There is an embedding Equiv(AB) , (A B).
 2 QInv(AB) Equiv(AB) over A B.
 3 Equiv(AB) QInv(AB) over A B.
 Here QInv(AB) is the nave type of quasi-invertible maps :
 QInv(AB) 
(f :A B) (g:B A) Id(g f 1A) Id(f g 1B)
 Univalence ( idtoeqv : IdU(AB) 
Equiv(AB) is an equivalence )
 can be stated equivalently using any such Equiv (but not QInv).
 But as soon as univalence holds, IdU also satis es these properties!
 Can univalence ever hold non-de nitionally?
What isde nitionalunivalence, really?
 Concretede nitionsofEquiv(AB) includemapsf :A Band
 g:B Aasdata. Itsuseful torememberexactlywhattheseare,
 de nitionally, tocomputewiththem.
 De nition
 Univalenceholdsde nitionally(at level1) if, forsomede nition
 Equiv(AB): (f:A B) (g:B A) wehave
 Equiv(AB) IdU(AB) Equiv(AB)
 suchthat(f g 1) (f g 2). (Perhaps 1 2.)
 Canalsoconsiderhigher levels,extractinghomotopiesaswell.
 Evencurrentcubical typetheories(CCHM,ABCFHL,CubicalAgda)
 donotsatisfythis!Cantevenextract f de nitionally.
One-to-onecorrespondences
 The best Equivisthetypeofone-to-onecorrespondences:
 1-1-Corr(AB): (R:A B U) (a:A)isContr( (b:B)R(ab))
 (b:B)isContr( (a:A)R(ab))
 Remark
 AnR:A B Uisacorrespondence. It isone-to-oneifeach
 elementofAorBhasexactlyonecorrespondent intheother.
 (Prefernottocall ita relation unless itsproposition-valued.)
 De nitionallysymmetricinAandB.
 Adirectpropositions-as-typesversionofclassical bijective
 relation (andreducestoitwhenABaresets), soitseasyto
 motivatewithouthomotopytheory.
 InalargeruniversethanAB...butsois IdU(AB).
 Alsoworksreallywell...
1-1 correspondences vs equivalences
 If R : A B Uis1-1, the centers of contraction yield
 f : A Bandg :B A,which form an equivalence.
 Conversely, if f : A 
B is an equivalence with inverse g : B 
we make a 1-1 correspondence by Rf(ab) : IdB(b fa).
 (b:B)IdB(b fa) is contractible with center (f a re fa).
 (a:A)IdB(b fa) is contractible with center (gb b).
 If we re-extract an equivalence, we get f and g de nitionally.
 With a fancier de nition of Rf , we can even remember the
 homotopies b : IdB(b fgb) and a : IdA(agfa).
 A,
Computing IdU
 For (philosophical, syntactic, and semantic) reasons (later), instead
 of IdU(AB) 1-1-Corr(AB), we make IdU primitive, with intro,
 elim, and but no . (Like a coinductive type with one destructor.)
 R : 1-1-Corr(AB)
 R : IdU(AB)
 A2 : IdU(A0A1)
 A2 :1-1-Corr(A0A1)
 p : 1-1-Corr(AB)
 p
 p
 This rule is su cient for de nitional univalence.
 Equiv(AB) 1-1-Corr(AB) IdU(AB) 1-1-Corr(AB) Equiv(AB)
Outline
 1 Background
 2 Identity types
 3 Function extensionality
 4 Univalence
 5 From univalence to homotopy theory
Towards-groupoid structure
 Now every A : U needs some re A : 1-1-Corr(AA). The obvious
 choice for its underlying correspondence is IdA : A 
A U:
 1(re A ) IdA
 The other parts of re A then give us singleton contractibility!
 1 2(re A ) : (a:A)isContr( (b:A)IdA(ab))
 2 2(re A ) : (b:A)isContr( (a:A)IdA(ab))
 In particular, this yields composition operations: given p : IdA(ax)
 and q : IdA(ay), we have (x p) (y q) : (b:A)IdA(ab). But
 (b:A)IdA(ab) is contractible, so we get (in particular)
 p 1 q: IdA(x y)
Computing-groupoid structure
 Now re is supposed to compute on all terms. And for U, the
 constructors are type formers. So we must specify how to
 compute, e.g., re A B using re A and re B.
 In the rst component, this is just the computation of identity types:
 re A B
 ( 1re A B
 (IdA B
 (IdA IdB
 ( 1re A
 2re A B )
 )
 )
 1re B
 )
 We give rules for the other components that compute the-groupoid structure of each type former, e.g. in A B
 (pq) 1 (r s) (p 1 r q 1 s)
Dependent identity types
 We can also apply non-nullary ap to terms in U.
 If z : A B :U and p : IdA(x y), we have
 apzB(p) : IdU(B(x)B(y))
 1(apzB(p) ) : B(x) B(y) U
 This is how we de ne the dependent/heterogeneous identity type:
 Idp
 zB(uv) :
 1(apzB(p) )(uv)
Rules for dependent identity types
 Since ap also computes on all terms, we give rules like
 Idp
 zB C(uv) Idp
 zB( 1u 1v) Idp
 zC( 2u 2v)
 The rule ap(re ) re implies that heterogeneous identity types
 over re reduce to homogeneous ones:
 Idre a
 zB (uv) IdB[a z](uv)
 Similarly, the rule apconstant(p) 
re
 implies that dependent
 identity types in constant families also reduce to homogeneous ones:
 Idp
 zB(uv) IdB(uv)
 (if z doesnt appear in B)
 Finally, functoriality of ap gives
 Idapx f (p)
 zC (uv) Idp
 xC[f z](uv)
Transport
 Still with z : A B : U and p : IdA(x y), we also have
 2(apzB(p) ) proving Idp
 B : B(x) 
B(y) Uis one-to-one.
 In particular, we have transport: each u : B(x) corresponds to some
 tr p
 zB(u) : B(y), with liftp
 zB(u) : Idp
 zB(u trp
 zB(u)).
 We must give computation rules for 2ap, specifying how transport
 computes on type families:
 tr p
 zB C(u) (trp
 zB( 1u) trp
 zC( 2u))
 liftp
 zB C(u) (liftp
 zB( 1u) liftp
 zC( 2u))
Deriving path induction
 As in cubical type theory, singleton contractibility and transport
 together imply Martin-Lof identity elimination J.
 1 Given C : (xy:A)IdA(x y) U with u : C(aa re a) and
 e : IdA(ab), singleton contractibility yields:
 q : Id (y:A)IdA(ay)((a re a) (be))
 2 Currying C to Ca : 
(y:A)IdA(ay)
 U, we can transport:
 tr q
 Ca
 (u) : Ca((be))
 C(abe)
 Again as in cubical type theory, the rule for J holds only typally.
and 
With dependent Id, we can de ne Id and Id :
 Id (x:A)B(x)(s t) 
(p:IdA( 1s 1t))Idp
 B( 2s 2t)
 Id (x:A)B(x)(f g) 
(x:A) (y:A) (p:IdA(xy))Idp
 B(f (x) g(y))
 with corresponding rules for ap on their term formers,
 and generalizations to dependent Id and Id .
Dependentmulti-variableapandId
 Dependent Idalsomakessenseofdependencies inn-aryap,using
 theevidentderivednotionofn-aryId.
 Eachidenti cationisdependentontheprecedingones.
 x1:A1 x2:A2(x1) xn:An(x1 xn 1) t :C(x1 xn)
 p1 : IdA1
 (a1 b1) p2 : Idp1
 x1A2
 (a2 b2) pn : Idp1 pn 1
 x1 xn 1An
 (an bn)
 apx1 xn t(p1 pn): Idp1 pn
 x1 xnC(t[a] t[b])
 Idp1 pn
 x1 xnC(uv): 1(apx1 xnC(p1 pn) )(uv).
 Whenformalizingthis,wemayuseaprimitivenotionoftelescope
 (acontextdependentontheambientcontext)










Towards third generation HOTT
 Part 2: Symmetries and semicartesian cubes
 Michael Shulman
 University of San Diego
 joint work with Thorsten Altenkirch and Ambrus Kaposi
 CMU HoTT Seminar
 May 5, 2022
Up today
 Plan for the three talks:
 1 Basic syntax of H.O.T.T.
 2 Symmetries and semicartesian cubes
 3 Semantics of univalent universes
Outline
 1 Acalculus of telescopes
 2 Some problems revealed by cubes
 3 Symmetry solves all problems
 4 Semicartesian cubes
 5 Semantic identity types
Review
 Last week I described the Book version of H.O.T.T., starting
 with simple ideas, and introducing complexity only as necessary.
 By way of review, lets reformulate the resulting theory more
 concisely and cleanly.
 In particular, we eventually ended up with n-variable ap (and Id)
 that bind a nite list of variables:
 x1 : A1
 xn : An t :B 
apx1 xnt(p1
 pn) : IdB( )
 Such a context su x is also called a telescope.
 We now reify these into a telescope calculus .
Telescopes
 Telescopes are de ned inductively as nite lists of types:
 tel
 tel
 A : U
 (
 x : A) tel
 The elements of a telescope are substitutions:
 () : 
: 
A : U a:A[ ]
 ( a): ( x :A)
 These are de ned mutually with their action on terms (and types):
 a : A
 : 
a[ ] : A[ ]
Dependent Idandapwithtelescopes
 Nowwecande neidentitytelescopesfromidentitytypes:
 tel : :
 Id ( )tel Id(() ())
 Id( x:A)(( a) ( a)) : Id ( ) : Id A(aa)
 Thesearede nedmutuallywithn-aryId,whichdependsonthem:
 : Id ( ) A:U a:A[ ] a :A[ ]
 Id A(aa):U
 WewriteIdA(aa) Id()
 A(aa) inthenon-dependentcase.
 (LasttimeIde neddependent Idintermsofap;herewepostulateit
 separatelyandthenmakethemcoincidelater.)
ComputingId
 Aswesawlasttime, Idcomputesonall typeformers:
 Id A B(s t) Id A( 1s 1t) Id B( 2s 2t)
 Id
 (x:A)B(s t) (q:Id A( 1s 1t))Id q
 ( x:A)B( 2s 2t)
 IdA B(f g) (u:A) (v:A) (q:Id A(uv))Id B(fugv)
 Id
 (x:A)B(f g) (u:A) (v:A) (q:Id A(uv))Id q
 ( x:A)B(fugv)
Id is a 1-1 correspondence
 All identity types are 1-1 correspondences:
 : Id ( ) 
corr A(a) : isContr
 A : U a:A[ ]
 (a:A[ ])Id A(aa)
 : Id ( ) 
A : U a :A[ ]
 corr A(a) : isContr (a:A[ ])Id A(aa)
 The centers of contraction constitute transport:
 : Id ( ) 
A : U a:A[ ]
 tr A(a) : A[ ]
 lift
 A
 (a) : Id A(a tr A(a))
 These witnesses compute on type formers:
 corr A B(a) 
hence also
 tr A B(a) 
,
 , etc.
Computingap
 AtermcanbeappliedtoIdofanytelescopeitdependson:
 : Id ( ) t :B
 ap t( ): Id B(t[ ] t[ ])
 Thishigher-dimensionalexplicitsubstitutioncomputesonall terms:
 ap (st)( ) (ap s( ) ap t( )
 ap 1s( ) 1ap s( ) ap 2s( ) 2ap s( )
 ap fb( ) ap f(p) b[a x] b[a x] ap b( )
 ap ( yt)( ) u v qap yt( q)
 Wede nere exivityasthe0-aryap: re a ap a().
Univalence
 IdU(AB) contains as a retract the type of 1-1 correspondences:
 1-1-Corr(AB) :
 1-1-Corr(AB) 
(R:A B U) (a:A)isContr( (b:B)R(ab))
 (b:B)isContr( (a:A)R(ab))
 IdU(AB) 1-1-Corr(AB)
 p p
 We identify dependent Id with ap into the universe:
 Id B(bb) 1(ap B( ) )(bb)
 corr B(bb) 
1 2(ap B( ) )(bb)
 corr B(bb) 
2 2(ap B( ) )(bb)
 (Last time, we de ned the LHS as the RHS. Separating them is more
 natural for Tarski universes, and permits types not lying in any universe.)
That asterisk: Neutral re exivities
 I claimed that ap is never a normal form, but theres one exception:
 When y is a variable, re y is neutral (hence normal).
 Since re is nullary ap, the rule that would apply is
 apx1 xny(p1
 pn) re y (if y is a variable 
x1
 where n = 0, but this just reduces re y ap()y() to itself!
 xn )
 This includes other terms that obviously must also be neutral:
 apxf(x)(p) 
re f (a0 a1 p) for a variable f : A B.
 IdA(a0 a1) ( 1re A)(a0 a1) for a variable A : U.
 Similarly, re re x
 , re re re x 
, etc., are also neutral.
Outline
 1 Acalculus of telescopes
 2 Some problems revealed by cubes
 3 Symmetry solves all problems
 4 Semicartesian cubes
 5 Semantic identity types
Squares and cubes
 H.O.T.T. is not a cubical type theory : there are no explicit cubes
 in the syntax. But like any other type theory with dependent identity
 types (including Book HoTT!), it has an emergent notion of cube:
 a02 : IdA(a00 a01)
 a12 : IdA(a10 a11)
 a21 : IdA(a01 a11)
 a22 : Ida02a12
 a20 : IdA(a00 a10)
 xy IdA(xy)(a20 a21)
 a12
 a10 a11
 a20
 a22
 a21
 a00 a01
 a02
 Similarly, IdIdIdA 
is a type of 3-dimensional cubes, etc.
 Very important point
 The roles of a02 a12 and a20 a21 are asymmetrical!
Cubical horn- llers
 Given a02 a12 a20, we have llers of left-to-right cubical horns:
 tr a02a12
 xy IdA(xy)(a20) : IdA(a01 a11)
 lifta02a12
 xy IdA(xy)(a20) : Ida02a12
 xy IdA(xy)(a20 tra02a12
 a10
 a20
 a12
 lifta02 a12
 xy IdA(xy)(a20)
 a00 a01
 a02
 xy IdA(xy)(a20))
 a11
 tr a02 a12
 xy IdA(xy)(a20)
 Similarly, tr and lift ll right-to-left cubical horns.
 And trIdIdA
 , etc. ll higher-dimensional left-right horns.
 Problem #1
 We dont seem to have top-to-bottom or bottom-to-top llers.
Degeneratecubes
 Givena2: IdA(a0 a1), therearetwodegeneratesquares:
 re a2
 : IdIdA(a0a1)(a2 a2) Idre a0 re a1
 xy IdA(xy)(a2 a2)
 apxre x
 (a2): Ida2
 xIdA(xx)(re a0
 re a1
 ) Ida2a2
 xy IdA(xy)(re a0
 re a1
 )
 a1 a1
 a0 a0
 re a1
 re a2
 re a0
 a2 a2
 a0 a1
 a0 a1
 a2
 apx re x(a2)
 a2
 re a0 re a1
Degeneratecubes
 Givena2: IdA(a0 a1), therearetwodegeneratesquares:
 a1 a1
 a0 a0
 re a1
 re a2
 re a0
 a2 a2
 a0 a1
 a0 a1
 a2
 apx re x(a2)
 a2
 re a0 re a1
 Problem#2
 Fora:A, thetwodoubly-degeneratesquares
 a a
 a a
 re a
 re re a
 re a
 re a re a
 a a
 a a
 re a
 apx re x(re a)
 re a
 re a re a
 seemtobede nitionallyunrelated.
Stuckdegeneraciesbreakcanonicity
 Problem#3
 Ourrulessofarcomputere a2
 basedonthestructureofa2,but
 apxre x
 (a2) isstuck,evenifa2 isveryconcrete.
 re x doesntreducewhenx isavariable.
 apdoesnt inspect its identi cationargument.
Stuckdegeneraciesbreakcanonicity
 Problem#3
 Ourrulessofarcomputere a2
 basedonthestructureofa2,but
 apxre x
 (a2) isstuck,evenifa2 isveryconcrete.
 re x doesntreducewhenx isavariable.
 apdoesnt inspect its identi cationargument.
 Abitnonobviously, thisalsobreakscanonicityforN.
 Intuitivehomotopy-theoreticreason
 ForatypeA:U, thesquareapxre x
 (re A) inUisessentiallya
 self-homotopyof theidentityequivalenceofA, i.e. (a:A)IdA(aa).
 TakingA=S1wegetastuckloopinIdS1(basebase),henceinZ.
 (Theresalsoanexplicitargumentusingtwouniverses insteadofS1.)
Outline
 1 Acalculus of telescopes
 2 Some problems revealed by cubes
 3 Symmetry solves all problems
 4 Semicartesian cubes
 5 Semantic identity types
Symmetry
 To solve these problems, we introduce a symmetry operation that
 transposes squares:
 a12
 a10 a11
 a20
 a22
 a00 a01
 a02
 a22 : Ida02a12
 a21
 a01 a11
 a21
 a02
 symA(a22)
 a12
 a00 a10
 a20
 xy IdA(xy)(a20 a21)
 symA(a22) : Ida20a21
 xy IdA(xy)(a02 a12)
TheotherKanoperations
 Nowwecan llothercubicalhorns, solvingproblem#1:
 a10 a11
 a00 a01
 a20
 a02
 a21
 a01 a11
 a00 a10
 a21
 a02
 a20
 a01 a11
 a00 a10
 a21
 lifta20 a21
 xy IdA(xy)(a02)
 a20
 a02 tr a20 a21
 xy IdA(xy)(a02)
 a10 a11
 a00 a01
 tr a20 a21
 xy IdA(xy)(a02)
 symA(lifta20 a21
 xy IdA(xy)(a02))
 a02
 a20 a21
Computing symmetry
 To solve problem #3, we de ne
 apxre x
 (a2) 
symA(re a2
 ).
 This computes based on a2...if sym also computes!
Computing symmetry
 To solve problem #3, we de ne
 apxre x
 (a2) 
symA(re a2
 ).
 This computes based on a2...if sym also computes!
 For the most part, computing symmetry is straightforward, e.g.:
 Ids02s12
 uv IdA B(uv)(s20 s21)
 Ids02s12
 uv IdA( 1u 1v) IdB( 2u 2v)(s20 s21)
 Ids02s12
 uv IdA( 1u 1v)( 1s20 1s21) Ids02s12
 Id 1s02 1s12
 uv IdB( 2u 2v)( 2s20 2s21)
 xwIdA(xw)( 1s20 1s21) Id 2s02 2s12
 yz IdB(yz)( 2s20 2s21)
 So we can de ne
 symA B((pq)) (symA(p) symB(q))
Dependentsymmetry
 Togeneralizethisto-types,weneeddependentsymmetryovera
 squareinatelescope(dontworrytoomuchaboutthesyntax):
 22: Id02 12
 Id ( )( 20 21) a22: Id02 12 22a02a12
 uv Id A(uv)
 (a20 a21)
 sym22
 A(a22): Id20 21sym( 22)a20a21
 uv Id A(uv)
 (a02 a12)
 Thenwecande ne
 sym22
 (x:A)B((pq)) (sym22
 A(p) sym22p
 ( x:A)B(q))
Symmetry for functions
 Idf02 f12
 f gIdA B(f g)(f20 f21) Idf02 f12
 f g (x0:A) (x1:A) (x2:IdA(x0 x1))IdB(fx0gx1)(f20 f21)
 (x00:A) (x01:A) (x02:IdA(x00x01))
 (x10:A) (x11:A) (x12:IdA(x10x11))
 (x20:IdA(x00x10)) (x21:IdA(x01x11)) (x22:Idx02 x12
 Idf02x02 f12x12
 uv IdB(uv)(f20x20 f21x21)
 So f22 : Idf02 f12
 xy IdA(xy)(x20x21))
 f gIdA B(f g)(f20 f21) is a function from squares in A, with
 arbitrary boundary, to squares in B with speci ed boundary.
 Thus we de ne symA B by transposing both input and output:
 symA B(f22)(x00 x10 x20 x01 x11 x21 x02 x12 x22)
 sym(f22(x00 x01 x02 x10 x11 x12 x20 x21 sym(x22)))
 Symmetry for-types is similar, using dependent symmetry.
Rules for symmetry
 Some obvious rules for symmetry are that it should be an involution:
 symA(symA(a22)) a22
 and it should commute with iterated ap on squares:
 symB(apapf 
(a22)) apapf 
(symA(a22))
 The nullary case of the latter is sym(re re a
 ) re re a
 .
 This solves problem #2:
 apxre x
 (re a) 
sym(re re a
 ) 
re re a
Higher-dimensional symmetry
 For n-dimensional cubes (i.e. n-fold iterated Id-types):
 We would expect symmetries to permute all n dimensions.
 The symmetric group Sn should act on n-cubes.
 We have transpositions of adjacent dimensions, from our sym.
 (E.g. symIdA 
: IdIdIdA 
IdIdIdA 
and apsymA 
: IdIdIdA 
Fortunately, Sn is generated by adjacent transpositions!
 Sn = 1 n 1
 k k =1
 j 
k = k j (j+1<k)
 k k+1 k = k+1 k k+1
 IdIdIdA 
.)
 The rst two relations follow from the equations on the last slide.
 To obtain the third, we assert
 symIdA
 (apsymA
 (symIdA
 (a222))) 
apsymA
 (symIdA
 (apsymA
 (a222)))
Outline
 1 Acalculus of telescopes
 2 Some problems revealed by cubes
 3 Symmetry solves all problems
 4 Semicartesian cubes
 5 Semantic identity types
Towards computation by gluing
 Symmetry computes the previously stuck term apxre x
 (a2).
 But how do we know there arent other stuck terms?
 Obviously, by proving canonicity/normalization.
 We havent done this yet, but the rst step (from a modern
 perspective) is constructing a set-based semantic model to be the
 codomain for Artin gluing.
Identity contexts
 Question
 What categorical structure corresponds to our identity types?
 The objects of a category C correspond to syntactic contexts.
 The fundamental operation on contexts takes to
 ID :
 : 
: 
: Id (
 )
 which factors the diagonal (i.e. is a path object):
 re
 ID
 ( :
 :
 This operation is functorial (via ap).
 ) = 
We have natural symmetries IDID = IDID , yielding an
 Sn-action on n-fold identity contexts..
Cubicalactions
 Thus,anID-structureonC isthesameas
 Afunctor ID:C C
 Nat. trans. r :1C IDands t : ID 1Cwithsr=tr=11C
 Natural symmetries ID ID=ID IDsatisfyingSn relations.
 De nition
 Let opbethemonoidalcategoryfreelygeneratedbyanobjectI,
 morphismsr :1 Iands t :I 1withsr=tr=11,where1is
 theunit,andsymmetriesI I=I IsatisfyingSn relations.
 ThenanID-structureonC isalsoequivalently
 Amonoidal functor op [CC]
 andthereforealsoequivalently
 Acoherentaction op C C.
The semicartesian cube category
 is a semicartesian monoidal category: symmetric monoidal
 and its unit 1 is terminal. Projections, but no diagonals.
 It is also the semicartesian monoidal category freely generated
 by an object I and morphisms s t : 1 I.
 We call the semicartesian cube category.
 This is the category used by:
 BernardyCoquandMoulin, for internal parametricity
 (actually they used a unary version, this would be the binary one)
 BezemCoquandHuber, for the original cubical model
 CavalloHarper, for the parametricity direction of parametric
 cubical type theory
Enrichment
 The presheaf category = Set op inherits a Day convolution
 monoidal structure (also semicartesian):
 k
 (X Y)n =
 Xk Y (nk )
 We write n for the representable ( I n). Note 0 is terminal.
 Theorem
 An action . : op C C is the same as an enrichment of C over
 that has powers by representables (write n X I n .X).
 Map(AB)n := C(A n B)
 (XMap(A n B))= (X nMap(AB))-enriched categories are the natural home for H.O.T.T. semantics.
Cubical objects
 Of course, 
is enriched over itself.
 Similarly, any category E op of cubical objects is-enriched, with
 powers and copowers if E is complete and cocomplete:
 k
 (A X)n =
 (A X)n =
 k
 (Ak 
(Xk)A
 ( m X)n=Xn m
 (nk )) X
 (kn )
 Map(XY)n = E op(X n Y)
More about the cube category
 Up to equivalence:
 The objects of are nite sets.
 A morphism 
(mn) is a function : n m
 that is injective on the preimage of m.
 The monoidal structure m n is disjoint union.
 Sometimes use a skeletal version with objects n = 01
 +
 n 1 ,
 but often the non-skeletal version with all nite sets is better.
 The coface k
 (n k n) is the identity on n k and
 sends k to .
 The codegeneracy k 
(nn k ) is the inclusion.
 The endomorphism monoid (nn) is the symmetric group Sn.
The magic of semicartesian cubes
 The monoidal structure of is almost cartesian; only the
 injectivity requirement spoils it. If it were cartesian we would have
 (nk )= (nk) (n ) ?
 Instead, we have
 (nk )=
 (n
 : (nk)
 (k) )
 Removing (k) from the second domain ensures the copaired
 function k 
n 
+ is still injective on the preimage of n.
 But in some ways this is even better!
Copowers by representables
 For A 
and X E op, we have
 k
 (A X)n =
 ( m X)n=
 k
 (Ak 
(nk )) X
 ( (km) (nk )) X
 =
 =
 =
 =
 (nm ) X
 (nm) (n (m) ) X
 (n
 (nm)
 Xn (m)
 (m) ) X
 (nm)
Semicartesian cylinders
 Taking m = 1, we get
 ( 1 X)n= 
A morphism 
Xn (1)
 (n1)
 (n1) is a function 1 n
 +, so either:
 some k n, in which case n (1) = n k , or
 + or , in which case n (1) = n. Thus:
 ( 1 X)n=Xn+Xn+
 Xn k
 k n
 An n-cube in 1 X is either an n-cube in the left-hand copy of X,
 an n-cube in the right-hand copy of X, or an (n 1)-cube in X
 stretched out in some dimension along the cylinder.
 There is almost no other cube category for which this holds.
Outline
 1 Acalculus of telescopes
 2 Some problems revealed by cubes
 3 Symmetry solves all problems
 4 Semicartesian cubes
 5 Semantic identity types
Semantic identity types
 In a-enriched category with representable powers, we also need:
 1 Coherence theorems.
 2 Transport and lifting ( brancy ).
 next time
 next time
 3 Categorical computation rules for Id, up to isomorphism.
Semantic identity types
 In a-enriched category with representable powers, we also need:
 1 Coherence theorems.
 2 Transport and lifting ( brancy ).
 next time
 next time
 3 Categorical computation rules for Id, up to isomorphism.
 Its tempting to think that, at least in , we can just de ne IdA B,
 IdA B, etc., to be whatever we want. But we cant: IdX must be
 de ned as 1 X. What we can de ne is the individual sets of
 n-cubes in a particular X 
. But:
 It can be non-obvious how these lead to a categorical
 characterization of the entire cubical set IdX.
 For type formers like A B, A B, we dont even have this
 much choice: they are determined by their universal properties.
 The computation rules for Id are non-trivial theorems about E op.
Identity types of products
 Note x : Ay : A IdA(x y) : U is represented semantically by the
 projection from the representable power 1 A A A.
 Since ( 1 
) is a right adjoint, it preserves products:
 1 
=
 (A B) ( 1 A) ( 1 B)
 (A B) (A B) (A A) (B B)
 =
 Syntactically, this gives
 IdA B(uv) = IdA( 1u 1v) IdB( 2u 2v)
 Same idea works for-types. A coherence theorem will improve = to =.
Up next
 Plan for the three talks:
 1 Basic syntax of H.O.T.T.
 2 Symmetries and semicartesian cubes
 3 Univalent universes



  A synthetic theory of-categories in homotopy type
 theory
 joint with Michael Shulman
 Octoberfest, Carnegie Mellon University
Motivation
 Why do I study category theory?
 — Ifind category theoretic arguments to be aesthetically appealing.
 What draws me to homotopy type theory?
 — Ifind homotopy type theoretic arguments to be aesthetically
 appealing.
Plan
 1. Homotopy type theory
 2. A type theory for synthetic 
3. Segal types and Rezk types
 4. The synthetic theory of-categories-categories
 Main takeaway: the dependent Yoneda lemma is a directed analogue of
 path induction in HoTT.
1
 Homotopy type theory
Types, terms, and type constructors
 Homotopy type theory has:
 • types A, B, …
 • terms x A, y B
 • dependent types x A ⊢ Bx type, x y A ⊢ Bx y type
 Type constructors build new types and terms from given ones:
 • products A B, coproducts A B, function types A B,
 • dependent sums ∑
 xABx , dependent products ∏
 xABx , and
 identity types x y A ⊢ x A y.
 Propositions as types:
 A B AandB
 A B AorB
 ∑
 ∏
 A B AimpliesB
 xA Bx
 xA Bx
 xBx
 xBx
 x Ay xequalsy
Identity types
 Formation and introduction rules for identity types
 x y A
 x Aytype
 x A
 reflx x A x
 ∑
 Semantics
 xreflx
 xyA x A y
 A A A
 ∆
 Hence ∑
 xyAx A y is interpreted as the path space of A and a term
 p x Aymay be thought of as a path from x to y in A.
Path induction
 The identity type family is freely generated by the terms reflx x A x.
 Path induction: If Bx y p is a type family dependent on x y A and
 p x Ay, then there is a function
 )
 path-ind 
(∏
 xA
 Bxx reflx
 ∏
 xyA
 ∏
 px Ay
 Bx y p
 Thus, to prove Bx y p it suffices to assume y is x and p is reflx.
 The-groupoid structure of A with
 • terms x A as objects
 • paths p x A yas 1-morphisms
 • paths of paths h p x Ay q as 2-morphisms, 
arises automatically from the path induction principle.
2
 A type theory for synthetic
 ( ,1)-categories
The intended model
 Set∆op ∆op
 bisimplicial sets
 Reedy 
types
 Segal
 types with
 composition
 Rezk
 types with
 composition
 & univalence
 Theorem (Shulman). Homotopy type theory is modeled by the
 category of Reedy fibrant bisimplicial sets.
 Theorem (Rezk). 
complete Segal spaces.-categories are modeled by Rezk spaces aka
Shapes in the theory of the directed interval
 Our types may depend on other types and also on shapes 2n,
 polytopes embedded in a directed cube, defined in a language
 ⊤
 and
 satisfying intuitionistic logic and strict interval axioms.
 ∆n 
∆
 Because ϕ 
t
 t
 t
 tn
 t
 2n tn 
2 t t
 t
 2 t t
 t
 ∆
 e.g.
 t t
 t
 t
 t
 t
 t
 implies ϕ, there are shape inclusions 
∆ 2
 t
 t
 t
 ∆ ∆.
Extension types
 shape inclusion: 
implies , i.e., so that 
t 
2n ϕ and
 .
 Formation rule for extension types
 shape
 A type
 ⟨ 
A a
 t 
2n 
so that ϕ
 ⟩
 a
 A term f 
⟨ 
A
 f 
⟩
 defines
 A so that f t
 a 
type
 a t for t 
A
 The simplicial type theory allows us to prove equivalences between
 extension types along composites or products of shape inclusions.
3
 Segal types and Rezk types
Hom types
 Formation rule for extension types
 shape
 ⊢ Atype
 ⟨ 
A a
 ⟩
 a 
type
 The hom type for A depends on two terms in A:
 x y A⊢homA x y
 A
 ∆ ∆ shape Atype x y ∆ A
 xy
 homA x y
 ⟨ 
∆ A
 ∆
 ⟩
 type
 A term f homA x y defines an arrow in A from x to y.
 ⟨
 xy
 ⟩
Segal types have unique binary composites
 A type A is Segal iff every composable pair of arrows has a unique
 composite, i.e., for every f homA x y and g homA y z the type
 ⟨ A
 fg
 ⟩
 is contractible.
 ∆
 Prop. A Reedy fibrant bisimplicial set A is Segal if and only if
 A∆2 ↠A 2
 1 has contractible fibers.
 fg
 Notation. Let compgf 
⟨ A
 ∆
 ⟩
 denote the unique
 inhabitant and write g ◦ f homA x z for its inner face, the composite
 of f and g.
Identity arrows
 For any x A, the constant function defines a term
 xx
 idx 
tx homA xx
 ⟨ 
∆ A
 ∆
 which we denote by idx and call the identity arrow.
 For any f homA x y in a Segal type A, the term
 idx f
 s t f t
 ⟨ A
 ∆
 ⟩
 ⟩
 witnesses the unit axiom f f ◦ idx.
Associativity of composition
 Let A be a Segal type with arrows
 f 
Prop.
 homA x y g homA y z h homA zw
 h ◦ g◦f
 h ◦g ◦f.
 Proof: Consider the composable arrows in the Segal type ∆
 f
 f
 x z
 h◦g
 f
 g◦f
 g◦f
 g
 y w
 Composing defines a term in the type ∆
 A:
 y
 g
 z
 g
 ℓ
 h◦g
 h
 h
 ∆
 A which yields a
 term ℓ homA xw so that ℓ h◦ g◦f andℓ h◦g ◦f.
Isomorphisms
 An arrow f homA x y in a Segal type is an isomorphism if it has a
 two-sided inverse g homA y x . However, the type
 ∑
 g ◦f idx
 g homA yx
 f ◦ g idy
 has higher-dimensional structure and is not a proposition. Instead define
 isisof
 ∑
 g homA yx
 g ◦f idx
 ∑
 h homA yx
 For x y A, the type of isomorphisms from x to y is:
 ∑
 x Ay
 isisof
 fhomA xy
 f ◦ h idy
Rezk types
 By path induction, to define a map
 id-to-iso
 x Ay x Ay
 for all x y A it suffices to define
 id-to-isoreflx
 idx
 ASegal type A is Rezk if every isomorphism is an identity, i.e., if the map
 id-to-iso
 is an equivalence.
 x Ay x Ay
Discrete types
 Similarly by path induction define
 id-to-arr
 ∏
 xyA
 x Ay homA x y by id-to-arr reflx idx
 and call a type A discrete if id-to-arr is an equivalence.
 Prop. A type is discrete if and only if it is Rezk and all of its arrows are
 isomorphisms. Thus, if the Rezk types are 
discrete types are-groupoids.
 Proof:
 id-to-arr-categories, then the
 x Ay homA x y
 id-to-iso
 x Ay
4
 The synthetic theory of
 ( ,1)-categories
Covariant fibrations I
 A type family x A ⊢ Bx over a Segal type A is covariant if for every
 f 
homA x y andu Bx there is a unique lift of f with domain u., i.e., if
 ∑
 vBy
 homB f u v iscontractible
 Here
 homB f u v
 ⟩
 ⟨ B f
 uv
 ∆ ∆
 is the type of arrows in B from u to v over f.
 B f B
 where
 ⌟
 ∆ A
 f
 Notation. The codomain of the unique lift defines a term f u By .
 Prop. For u Bx , f homA x y , and g homA y z ,
 g f u g◦f u and idx u u
Covariant fibrations II
 A type family x A ⊢ Bx over a Segal type A is covariant if for every
 f 
homA x y and u Bx there is a unique lift of f with domain u.
 Prop. If x A ⊢ Bx is covariant then for each x A the fiber Bx is
 discrete. Thus covariant type families are fibered in-groupoids.
 Prop. Fix a A. The type family x A ⊢ homA ax is covariant.
 For u homA ax and f homA x y , the transport f u equals the
 composite f ◦ u as terms in homA a y ., i.e., f u
 f ◦ u.
The Yoneda lemma
 Let x A ⊢Bx be a covariant family over a Segal type and fix a A.
 Yoneda lemma. The maps
 ev-id 
and
 yon 
ϕϕa ida
 )
 (∏
 xA
 homA ax Bx
 u x f f u Ba
 (∏
 Ba
 )
 homA ax Bx
 xA
 are inverse equivalences.
 Proof: The transport operation for covariant families is functorial in A
 and fiberwise maps between covariant families are automatically natural.
 Note. A representable isomorphism ϕ ∏
 xA homA ax
 homA bx
 induces an identity ev-idϕ b A a if the Segal type A is Rezk.
The dependent Yoneda lemma
 From a type-theoretic perspective, the Yoneda lemma is a
 “directed” version of the “transport” operation for identity types.
 This suggests a “dependently typed” generalization of the Yoneda
 lemma, analogous to the full induction principle for identity types.
 Dependent Yoneda lemma. If A is a Segal type and Bx y f is a
 covariant family dependent on x y A and f homA x y , then
 evaluation at xx idx defines an equivalence
 ev-id 
∏
 ∏
 xyA
 fhomA xy
 Bx y f
 ∏
 xA
 Bxx idx
 This is useful for proving equivalences between various types of
 coherent or incoherent adjunction data.
Dependent Yoneda is directed path induction
 Takeaway: the dependent Yoneda lemma is directed path induction.
 Path induction: If Bx y p is a type family dependent on x y A and
 p x Ay, then there is a function
 )
 path-ind 
(∏
 xA
 Bxx reflx
 ∏
 xyA
 ∏
 px Ay
 Bx y p
 Thus, to prove Bx y p it suffices to assume y is x and p is reflx.
 Dependent Yoneda Lemma: If Bx y f is a covariant family dependent
 on x y Aandf homA x y andAis Segal, then there is a function
 )
 id-ind 
(∏
 xA
 Bxx idx
 ∏
 xyA
 ∏
 fhomA xy
 Bx y f
 Thus, to prove Bx y f it suffices to assume y is x and f is idx.
References
 For considerably more, see:
 Emily Riehl and Michael Shulman, A type theory for synthetic-categories, arXiv:1705.07442
 To explore homotopy type theory:
 Homotopy Type Theory: Univalent Foundations of Mathematics,
 https://homotopytypetheory.org/book/
 Michael Shulman, Homotopy type theory: the logic of space,
 arXiv:1703.03007
 Thank you

Towards an Implementation of
 Higher Observational Type Theory
 Michael Shulman
 University of San Diego
 jww Thorsten Altenkirch, Ambrus Kaposi, and Elif Uskuplu
 running HoTT @ NYU Abu Dhabi
 20 April 2024
Outline
 1 Introduction
 2 Some choices about the theory
 3 Normalization by evaluation
 4 Higher-dimensional normalization
What is Higher Observational Type Theory?
 H.O.T.T. is a third style of homotopy type theory, after Book HoTT
 and Cubical Type Theory.
 • In Book HoTT, identity types are defined uniformly across all
 types as an inductive family.
 • In Cubical Type Theory, identity types are defined uniformly
 across all types by mapping out of the interval.
 • In Higher Observational Type Theory, identity types are defined
 observationally according to the base type.
 • IdA× B(⟨x0,y0⟩,⟨x1,y1⟩) is a product IdA(x0,x1) × IdB(y0,y1).
 • IdA→B(f0,f1) is (x : A) → IdB(f0 x,f1 x)
 (x0 x1 : A)(x2 : IdA(x0,x1)) → IdB(f0 x0,f1 x1)
 • IdU(A,B) is a type of equivalences A ≃ B.
 HOTT has natural semantics in semicartesian (BCH) cubical sets.
The primitives of HOTT
 1 Any type A has an identity type IdA(x0,x1), which computes∗
 based on the structure of A.
 2 Any term M : A has a reflexivity term reflM : IdA(M,M),
 which computes based on the structure of M.
 • refl⟨a,b⟩ = ⟨refla,reflb⟩ and reflfstu = fstreflu, etc.
 • reflλx.M = λx0x1x2.apx.M(x0,x1,x2), etc.
 3 Any open term x : A ⊢ M : Bx has an apx.M(a0,a1,a2), for
 a2 : IdA(a0,a1), which computes based on M.
 • apx.⟨M,N⟩(a0,a1,a2) = apx.M(a0,a1,a2),apx.N(a0,a1,a2)
 • apx.λy.M(a0,a1,a2) = λy0 y1 y2.ap(x,y).M(a0,a1,a2,y0,y1,y2)
 • apx.MN(a0,a1,a2) =
 apx.M(a0,a1,a2) N[x →a0] N[x →a1] apx.N(a0,a1,a2)
 (This is what requires our definition of IdA→B.)
 4 Any square a22 : Ida02,a12
 sym(a22) : Ida20,a21
 IdA
 (a20, a21) has a symmetry
 (a02, a12), which computes based on a22.
 IdA
From parametric type theory to HOTT
 Cubical Type Theory can be obtained by defining a fibrancy
 predicate in a non-univalent substrate theory (Orton–Pitts).
 We intend to obtain HOTT similarly. The rule
 IdA→B(f0,f1) is (x0x1 : A)(x2 : IdA(x0,x1)) → IdB(f0 x0,f1 x1)
 suggests that the substrate should be internal binary parametricity,
 where Id is a “bridge type”. This satisfies all the same rules as the
 identity type in HOTT except
 • IdU(A,B) is a type of correspondences A → B → U.
What we want
 What we want
 1 A proof assistant implementing HOTT!
 For that we need...
 2 A typechecking algorithm
 For that we need (as for any dependent type theory)...
 3 An equality-testing algorithm
 And for that we need (more or less)...
 4 A normalization algorithm (computing with open terms).
 Roughly speaking, we test equality by normalizing both terms and
 comparing normal forms.
What we have
 To be presented today
 1 A normalization algorithm for a version of “Parametric OTT”.
 2 An implementation of this algorithm in OCaml, along with a
 typechecker for a prototype proof assistant called Narya.
 NOT being presented today
 A proof that this algorithm is correct!
 However:
 • The algorithm aligns with general principles of NbE.
 • The implementation is very strongly typed, so it serves as a
 partial formalization of correctness.
 • Narya has been tested on many examples and seems to work.
Outline
 1 Introduction
 2 Some choices about the theory
 3 Normalization by evaluation
 4 Higher-dimensional normalization
Higher-dimensional structure
 The higher structure of HOTT is generated by low-dimensional
 primitives like “refl” and “sym”. But many different such
 composites produce the same operation.
 Image credit: John Baez
 sym(apsym(sym(x222)))
 ≡apsym(sym(apsym(x222)))
 A normalization algorithm must implement such equalities.
 Our choice
 Represent higher dimensions directly internally, evaluating each
 composite of refl and sym to a cubical operator in canonical form.
 The user can still restrict themselves to refl and sym.
Σ-types vs records
 The identity type of a Σ-type is “defined to be” another Σ-type:
 IdΣ(x:A).B(x)(u, v) ≈ Σ(p : IdA(π1u,π1v)).Idp
 B(π2u,π2v)
 In a proof assistant, Σ-types are just a particular record type:
 def Σ (A : Type) (B : A → Type) : Type := sig (
 fst : A,
 snd : B fst,
 )
 In general, the identity type of any record type should be another
 record type, but it can’t be an instance of the same record type.
 And similarly for inductive and coinductive types.
(Non-)computation with types
 Our choice
 Refrain from computing definitionally with any identity types.
 For example Id (Σ A B) u v is not definitionally equal to
 Σ (Id A (u .fst) (v .fst))
 (p → Id B (u .fst) (v .fst) p (u .snd) (v .snd))
 but instead behaves like a record type defined as
 sig (
 fst : Id A (u .fst) (v .fst),
 snd : Id B (u .fst) (v .fst) fst (u .snd) (v .snd),
 )
 They are definitionally isomorphic, and their fields and constructors
 have the same names, so we can usually pretend they are the same.
 Inductive, coinductive, and even function types are similar.
Outline
 1 Introduction
 2 Some choices about the theory
 3 Normalization by evaluation
 4 Higher-dimensional normalization
Old-style normalization
 Old view of normalization
 1 Formulate reduction rules such as (λx.M)N ⇝ M[x → N]
 2 Prove that applying these reductions to any term eventually
 leads to a normal form, a term that cannot be further reduced.
 However, this is not very efficient. For example:
 (λx.λy.M)N P ⇝ (λy.M)[x → N] P
 ≡ λy.M[x → N] P
 ⇝M[x →N] [y →P]
 We have to traverse the term M (which could be large) twice:
 once to substitute N for x, then again to substitute P for y.
 (Also worry about variable capture, or incrementing De Bruijn indices, etc.)
TowardsNbE
 First idea
 Don’tactuallycompute(λy.M)[x→N],butkeepitasaclosure.
 Then,whenit isappliedtoafurtherargumentP,computethe
 simultaneoussubstitutionM[x→N,y→P].
 However, if itnever isappliedtoafurtherargument,wedohaveto
 actuallycomputeitasλy.M[x→N] togetanormal form.
 Totrackthis,andensurethatclosuresneverappear innormal
 forms,weusetwodifferentkindsofterms:
 • termsdonotcontainclosures,anduseDeBruijnindices.
 • valuescontainclosures,anduseDeBruijnlevels.
 (Useof levels/indiceseliminatesvariablecaptureandindexincrements.)
Normalization by evaluation
 Normalization has two steps:
 1 evaluation of a term M into a value, using an environment that
 assigns a value to every free (index) variable in M.
 2 readback of a value into a normalized term.
 In particular:
 • There is no “substitution” operation: evaluation does it all.
 • When readback finds a closure (λy.M)[x → N], it restarts
 evaluation with y bound to a variable, M[x → N, y → y], then
 reads back the result and re-wraps it in λy.
 • Readback can be type-directed and perform η-expansion.
 • If we define the type of values to contain no redexes, we can
 guarantee statically that the result is a normal form.
 • There’s a close connection to mathematical proofs by
 categorical gluing along a restricted Yoneda embedding.
Outline
 1 Introduction
 2 Some choices about the theory
 3 Normalization by evaluation
 4 Higher-dimensional normalization
Matchingunderbinders
 InordinaryNbE,matchinghappensduringevaluation.
 Example
 Toevaluatetheterm“ifMthenNelseP”,wefirstevaluateMtoa
 valueandinspecttheresult. If it is“true”,weproceedtoevaluate
 N; if it is“false”,weproceedtoevaluateP.
 However, thisstyledoesn’tplaywellwithmatchingunderbinders.
 Example
 Toevaluate“apx.M(p0,p1,p2)”,wehavetoinspectMto
 implementrules likeforpairs:
 apx.⟨M,N⟩(p0,p1,p2)≡ apx.M(p0,p1,p2),apx.N(p0,p1,p2)
 Butevaluatingx.Mproducesaclosure,notactuallycomputingthe
 bodyMtoanythingwecanmatchagainst!
ap is a form of substitution
 “ap” is a lot like substitution:
 1 They are never∗ normal forms: they always reduce away,
 computing on both introduction and elimination forms.
 2 The user doesn’t need direct access to them. For “ap”, it
 suffices to use “refl” on a function.
 apx.M(p0,p1,p2) ≡ reflλx.M p0 p1 p2
 3 Their computation rules are similar:
 ⟨M,N⟩[x → P] ≡ M[x → P],N[x → P]
 Thus, we replace “ap” by a higher-dimensional substitution, which
 in NbE becomes higher-dimensional evaluation.
Higher-dimensional environments
 Definition
 An n-dimensional environment associates to each (index) variable an
 n-dimensional cube of values.
 n =0 a:A
 n =1 a0:A,a1:A, a2 : IdA(a0,a1)
 n =2 a00:A, a01 :A, a02 : IdA(a00,a01),
 a10 : A, a11 : A, a12 : IdA(a10,a11),
 a20 : IdA(a00,a10), a21 : IdA(a01,a11),
 a22 : Ida02,a12
 IdA
 (a20, a21)
Faces and evaluation
 For any k-dimensional face ϕ of an n-dimensional cube, an
 n-dimensional environment θ has a k-dimensional face environment
 θ ∗ϕ. E.g. the faces of the 1-dimensional
 
  
x→ a0:A, a1 :A, a2 : IdA(a0,a1) ,
 y → b0 :B, b1 : B, b2 : IdB(b0,b1)
 
 
 are the 0-dimensional [x → a0, y → b0] and [x → a1, y → b1].
 Evaluating a term M in an n-dimensional environment θ produces
 an n-dimensional value M[θ], whose boundary consists of M[θ ∗ ϕ]
 for the faces ϕ of n. For example, if ⟨x,y⟩ : A × B, then
 ⟨x, y⟩ x → (a0,a1,a2),y → (b0,b1,b2) ≡ ⟨a2,b2⟩
 which lies in IdA×B(⟨a0,b0⟩,⟨a1,b1⟩).
ap is higher evaluation
 Now instead of apx.M(a0,a1,a2) we have
 M[x → (a0,a1,a2)].
 In particular, the computation rule for reflexivity of an abstraction,
 which “starts” higher substitution, is
 reflλx.M ≡ λx0x1x2.M[x → (x0,x1,x2)].
 In NbE, this should be an evaluation rule in some environment θ.
 But if θ starts out 0-dimensional, we need to evaluate M in a
 1-dimensional environment that we can extend by (x0,x1,x2).
 reflλx.M[θ] ≡ λx0 x1 x2.M[?,x → (x0,x1,x2)]
 We need an operation of “degenerate environments”.
ap is higher evaluation
 Now instead of apx.M(a0,a1,a2) we have
 M[x → (a0,a1,a2)].
 In particular, the computation rule for reflexivity of an abstraction,
 which “starts” higher substitution, is
 reflλx.M ≡ λx0x1x2.M[x → (x0,x1,x2)].
 In NbE, this should be an evaluation rule in some environment θ.
 But if θ starts out 0-dimensional, we need to evaluate M in a
 1-dimensional environment that we can extend by (x0,x1,x2).
 reflλx.M[θ] ≡ λx0 x1 x2.M[reflθ,x → (x0,x1,x2)]
 We need an operation of “degenerate environments”.
Degeneracies
 Any m-dimensional degeneracy δ of an n-dimensional cube maps an
 n-dimensional object M to an m-dimensional one M⟨δ⟩. E.g.
 reflM ≡M⟨ρ⟩ symM ≡M⟨σ⟩
 Like substitution/evaluation, M⟨δ⟩ is defined by traversing M.
 But unlike evaluation, both M and M⟨δ⟩ are values.
 This is necessary to evaluate degeneracies:
 (reflx)[x → M] ≡ M⟨ρ⟩
 where M, being in an environment, is a value.
 (NB: For afficionados of modal type theory, θ ∗ ϕ and M⟨δ⟩ may remind you of
 locks and keys.)
Degenerate environments
 An m-dimensional degeneracy δ of an n-dimensional cube also maps
 any n-dimensional environment θ to a degenerate environment θ ∗ δ.
 For instance, [x → a,y → b] ∗ ρ (reflexivity) is
 
  
x→ a:A, a:A, refla : IdA(a,a) ,
 y → b:B, b :B, reflb : IdB(b,b)
 This is how we evaluate degeneracies in general:
 (M⟨δ⟩)[θ] ≡ M[θ ∗δ].
 And act on closures by degeneracies:
 (λy.M)[θ] ⟨δ⟩ ≡ (λy.M)[θ ∗ δ]
 
 
 In particular, the actual evaluation of reflexivity of an abstraction is
 (λx.M)⟨δ⟩ [θ] ≡ (λx.M)[θ ∗ δ]
 which is, of course, a closure and doesn’t go under the λ until
 applied or read back.
Some categorical remarks
 In combination, environments are acted on by arbitrary morphisms
 in the BCH cube category (composites of faces and degeneracies).
 θ ∗(ϕ◦δ) = (θ∗ϕ)∗δ
 In an algebraic presentation, substitutions (∼ environments) are
 indexed by a dimension:
 θ : Γ n −→ ∆
 and are acted on by morphisms in the cube category:
 θ : Γ n −→ ∆
 ψ : m→n
 θ ∗ψ : Γ m −→ ∆
 Thus, we have a cubical set of substitutions from Γ to ∆. That is,
 The category of contexts is enriched over cubical sets.
 We thus expect an enriched version of categorical gluing to appear
 in a formal proof of normalization.
Higher-dimensional NbE
 With these modifications...
 . . . and a lot of omitted work and details...
 . . . we get a normalization by evaluation algorithm.
 degeneracies
 terms
 eval
 values
 readback
 normals
 Using this for equality-checking, we then implement a typechecker.
 https://github.com/mikeshulman/nary












What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Thinking Recursively, Rethinking Corecursively
 David Jaz Myers
 June 19, 2017
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Mathematical Metaphors
 This talk will be about two specific mathematical metaphors, but
 what are mathematical metaphors,
 why make them,
 and how can they be misused?
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Mathematical Metaphors
 In this talk, we will look closely at the mathematical metaphor
 between
 Complex Systems and Recursive Functions
 Wewill see how this metaphor a lot of standard theories in science
 and philosophy, usually those that fall under the rubrik of “realism”.
 Wewill also find that this metaphor can lead us to some shaky
 philosophical positions.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 What is a function
 A function is a process that turns an input into an output.
 F(input) = output
 If a function takes inputs of a type Inputs and gives outputs of a
 type Outputs, we write
 F : Inputs Outputs
 For example,
 F : Numbers Numbers
 F(n) = 2n +1
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 What is Recursion?
 A function is recursive when its output on a complicated input is
 determined by its output on simpler inputs.
 Ultimately, the output of a recursive function is determined by its
 simplest inputs.
 Wecall these simplest inputs atoms, or base cases, and the rules
 for building them up constructors.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 What is Recursion?
 So to define a recursive function we need
 to know how to break apart complicated inputs into simpler
 ones,
 simplest inputs (so we eventually stop breaking things apart),
 to know how to put outputs together in a way that relates to
 taking inputs apart!
 Or, more pithily, we need:
 to know how to analyze inputs,
 into their atomic components,
 so that we can construct outputs.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 A Lengthy Example
 Let’s calculate the length of a list! This is a function which takes a
 list as input and gives a number as output.
 Length : Lists Numbers
 A list is something like:
 [first item, second item, third item
 Wecan break down a list like this:
 last item]
 AList = [first item, Rest of the List]
 or the list is Empty.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 A Lengthy Example
 Let’s calculate the length of a list! This is a function which takes a
 list as input and gives a number as output.
 Length : Lists Numbers
 Numbers can be built up by counting:
 0 is a number, and
 (1 +anumber) is a number.
 This is related to taking lists apart because, secretly, numbers are
 like lists of tally marks:
 4 =
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 A Lengthy Example
 Definition (Length of a List)
 The length of a list is given by the function defined by:
 Length(Empty) 0
 Length([first itemRest of List]) 1 + Length(Rest of List)
 This works because
 Empty is an atom. There are no simpler lists, so we can stop
 breaking things apart.
 The Rest of the List is simpler (i.e. smaller) than the list we
 started with. This means we eventually get to the Empty list.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Running a Recursive Program
 Wecan run a recursive program greedily:
 Every time we see something we don’t understand, we compute it.
 Length([123]) = 1+Length([23])
 =1+(1+Length([3]))
 =1+(1+(1+Length(Empty)))
 =1+(1+(1+0))
 =1+(1+1)
 =1+2
 =3
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Thinking Recursively About Everything
 This way of thinking should be familiar to you from popular ways of
 thinking about physics.
 Claim
 Physics is like a recursive function
 Physics : Systems Systems
 which recurses all the way to the fundamental particles, and then
 builds more complicated phenomena out of the way they behave.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Thinking Recursively About Everything
 Or from philosophy of language:
 Claim
 Meaning is like a recursive function
 Meaning : Utterances Meanings
 which builds the meaning of, say, sentences out of the meaning of
 words.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Thinking Recursively About Everything
 Or from sociology
 Claim
 A society is like a recursive function
 Society : Societies 
Societies
 which is determined by the behavior of individuals which are, of
 course, indivisible.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Thinking Recursively About Everything
 Or from economics
 Claim
 The economy is like a recursive function
 Economy : Markets Markets
 which is determined by the behavior of agents who act rationally.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Analysis is Recursive
 Definition
 [Analysis] might be defined as a process of isolating or
 working back to what is more fundamental by means of
 which something, initially taken as given, can be
 explained or reconstructed.– Stanford Encyclopedia
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 A Philosophical Problem
 In his book The Case for Idealism, John Foster argues that some
 things must have inscrutable, intrinsic properties.
 Foster’s argument for inscrutable intrinsic properties
 Suppose that all properties of all things were extrinsic, that is,
 defined in relation to other things.
 A)
 (B
 Now, consider a world containing two things, A and B, each
 defined only by their disposition to repel the other.
 Foster claims this leads to an infinite regress, and therefore a
 contradiction.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 A Philosophical Problem
 Foster’s argument for inscrutable intrinsic properties (cont’d)
 The back and forth must stop somewhere:
 “A is the thing which 
X”
 X is the end of the line, it is not defined in relation to anything else.
 Therefore, it is both
 inscrutable, and
 intrinsic.
 This argument rests on two (recursive) assumptions:
 1 Wemust ‘evaluate’ greedily.
 2 There must be a base case.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Do WeHaveto Make Those Assumptions?
 is there another way?
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Corecursion
 A function is corecursive when its output is determined by simpler
 outputs.
 Wecall the rules for breaking apart the output observers.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 What is Corecursion
 So, to define a corecursive function we need
 to know how to observe the output of our function in simpler
 ways,
 that relate to how we observe our inputs!
 Wecan think of the observers as being experimental setups with
 which we will test the output of our function.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 What is Corecursion
 The main idea behind corecursion is:
 If we know how our function behaves in all experimental
 setups, we know what it does.
 This is essentially the same as one of the fundamental principles
 of science:
 If we can predict how something behaves in all experimental
 setups, then we know what it is.
 So long as we believe that a function is what it does.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Stream and Chill
 Let’s have some fun with streams to get our heads around
 corecursion.
 A stream is an infinite list, so we can’t keep the whole thing in
 memory, but we can observe it piece by piece.
 So, let’s set up two experiments:
 1 Head, where we test what the first thing in the stream is.
 2 Tail, where we see what’s left.
 Now wecan define functions corecursively, since we know how to
 observe their behavior.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Stream and Chill
 Let’s define a function
 Every Other : Streams Streams
 that will take a stream and return the stream of only every other
 value. For example:
 Every Other(01234 )=(024 )
 To define this, we just need to define how it looks in all the
 experiments.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Stream and Chill
 Definition (The Every Other Function)
 Define the Every Other function by
 EO(stream)Head = streamHead
 EO(stream)Tail = EO(streamTailTail)
 This works because
 EO(stream) is covered by the observers Head and Tail, they
 tell us all we need to know about it.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Running a Corecursive Program
 Wecan’t evaluate a corecursive program greedily, because the
 calculation would never end! We have to be lazy:
 Only compute things when we absolutely need to.
 So if you wrote down
 EO((0123 ))
 That would be totally chill.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Running a Corecursive Program
 But, if we want to know a specific value of EO((0123 )), then
 we can calculate
 EO((0123 ))TailTailHead
 =EO((0123 )TailTail)TailHead
 =EO((0123 )TailTailTailTail)Head
 =(0123 )TailTailTailTailHead
 =(1234 )TailTailTailHead
 =(2345 )TailTailHead
 =(3456 )TailHead
 =(4567 )Head
 =4
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Corecursion and Diff´ erance
 If someone asks you what “EO” means, you could tell them that its
 meaning is deferred until we test it with the observers Head and
 Tail.
 If they ask you what “Head” and “Tail” mean, you could only tell
 them the different ways you end up using them.
 Definition
 Diff´ erance is Derrida’s pun on the words defer and differ.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Thinking Corecursively
 Who amI?
 How can I find out?
 Do I have to find my ‘true self’, the core of my being, to know who I
 am?
 Or do I only have to look at the way I affect the people and places
 around me?
 Thinking corecursively, we don’t have to be anxious about finding
 our true selves.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Revisiting Foster
 Let’s look back at Foster’s argument for inscrutable intrinsic
 properties. He claims that the world in which
 A only repels B and B only repels A
 cannot exist because it leads to an infinite regress.
 Only leads to infinite regress if we are greedy.
 If we are lazy, this is a perfectly fine definition.
 There is nothing inscrutable about it.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Revisiting Foster
 Foster’s argument shows a fundamental confusion that often
 underlies recursive thinking:
 the confusion between names and things
 Names are like atoms, we don’t break them apart.
 Things (such as functions) can be named, even when we
 define them corecursively.
 But that doesn’t mean that they have base cases!
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Limits of the Metaphor
 To define a function corecursively, we must cover it by observers.
 Head and Tail tell us all there is to know about a stream.
 But in the informal world, we never have access to all the contexts
 in which an object appears,
 Wecan never get all sides of the story.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Going Forward: Physics
 Physicists have been thinking corecursively for a long time:
 A physical quantity can only be assigned specific values given
 a local coordinate system, or gauge.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Going Forward: Physics
 Principle of Relativity
 The physical laws have the same form in all choices of gauge.
 A change in gauge is called a gauge symmetry.
 In other words, if we rotate our experimental setup, we get a
 rotated result.
 r(X) = r( X)
 The relationship between the observations X and r(X)
 depends on how X was rotated to r(X).
 To fully know an object, we must not only know how it behaves in
 various contexts,
 we must also know how those contexts relate.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 In Conclusion
 Thinking recursively makes us believe that
 There are basic objects and basic truths about them at the
 bottom of all phenomena, and
 To know anything at all, we need to know about these basic
 things.
 Thinking corercursively makes us believe that
 Things only make sense in context (in an experiment, relative
 to an observer, etc.), and
 Knowing how a thing behaves in context is all there is to know
 about it
 There are no basic objects or basic truths
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Bridging the Divide
 In this talk, I made a stark division between recursive and
 corecursive thinking.
 But in actually programming languages (like Haskell), you can use
 recursion and corecursion together depending on which is more
 convenient.
 Weshould use recursive and corecursive thinking together,
 depending on what needs to be done.
 But most importantly, we need to remember that metaphors matter.
 Don’t get trapped in a single metaphor
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 References I
 AndreasAbel, Brigitte Pientka, David Thibodeau, and Anton
 Setzer, Copatterns: Programming infinite structures by
 observations, SIGPLAN Not. 48 (2013), no. 1, 27–38.
 MichaelBeaney, Analysis, The Stanford Encyclopedia of
 Philosophy (Edward N. Zalta, ed.), spring 2015 ed., 2015.
 J.Rutten. C. Kupke, M. Niqui, Stream differential equations:
 concrete formats for coinductive definitions., Technical Report
 No. RR-11-10 (2011), 1– 28.
 BarryDainton, Time and space: Second edition,
 Mcgill-Queens University Press, 2010.
 DexterKozen and Alexandra Silva, Practical Coinduction,
 2014.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 References II
 J.Rutten, An introduction to (co)algebra and (co)induction.,
 Advanced topics in bisimulation and coinduction. (D. Sangiorgi
 and J. Rutten, eds.), Cambridge University Press, Cambridge,
 2011.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively














































 Towards third generation HOTT
 Part 3: Univalent universes
 Michael Shulman
 University of San Diego
 joint work with Thorsten Altenkirch and Ambrus Kaposi
 CMU HoTT Seminar
 May 12, 2022
The story so far
 Plan for the three talks:
 1 Basic syntax of H.O.T.T.
 2 Symmetries and semicartesian cubes
 3 From semicartesian cubes to univalent universes
Outline
 1 The magic of semicartesian cubes
 2 Paths in exponentials
 3 The parametricity universe
 4 The universe of brant types
 5 Cubical spaces
 6 Explaining the universe
The semicartesian cube category
 The semicartesian cube category has, as objects, nite sets.
 A morphism 
(mn) is a function : n m
 +
 that is injective on the preimage of m.
 The symmetric monoidal structure m n is disjoint union.
 The automorphisms of n are the symmetric group Sn.
 The presheaf category = Set op has a Day convolution
 monoidal structure. Write n for the representable ( n).
 A-enriched category with n-powers has ID-structure:
 1 
x : Ay :A IdA(x y):U
 A
 A A
Cubical paths and cylinders
 Let E be a presheaf category (such as Set). The category E op of
 cubical objects is-enriched with copowers and powers:
 (KMapE op(XY)) = E op(K XY)=E op(XK Y)
 In particular, it has path spaces 1 X and cylinders 1 X.
 Path spaces are de ned by shifting, while cylinders are magic:
 ( 1 X)n=Xn 1
 ( 1 X)n=Xn+Xn+
 Xn k
 k n
 =2 Xn+n Xn 1
 Almost no other cube category satis es the magic cylinder formula;
 we need symmetries but no diagonals or connections.
The magic of semicartesian cylinders
 For example:
 ( 1 X)2=X2+X2+X1+X1
The magic of semicartesian cylinders
 For example:
 ( 1 X)2=X2+X2+X1+X1
The magic of semicartesian cylinders
 For example:
 ( 1 X)2=X2+X2+X1+X1
The magic of semicartesian cylinders
 For example:
 ( 1 X)2=X2+X2+X1+X1
The magic of semicartesian cylinders
 For example:
 ( 1 X)2=X2+X2+X1+X1
The magic of semicartesian cylinders
 For example:
 ( 1 X)2=X2+X2+X1+X1
 2
 1
 1
 2
 2
 1
 2
 1
The magic of semicartesian cylinders
 For example:
 ( 1 X)2=X2+X2+X1+X1
 2
 1
 1
 2
 2
 1
 2
 1
Amazing right adjoints
 Since the path-space is shifting, ( 1 X)n = Xn 1, it preserves all
 colimits, hence has an ( amazing ) right adjoint
 E op( 1 XY)=E op(X Y)
 This also has a berwise version:
 Y
 1 
W
 YW Y
 W
 1 
W
 The berwise version maps E op ( 1 W) to E opW.
Outline
 1 The magic of semicartesian cubes
 2 Paths in exponentials
 3 The parametricity universe
 4 The universe of brant types
 5 Cubical spaces
 6 Explaining the universe
Identity types of exponentials
 For cartesian cubes, powers coincide with cartesian exponentials. So
 1 
(A B)=A ( 1 B),andIdA B(f g)= (x:A)IdB(fx gx).
 exponential A 
In the semicartesian case, we need to relate the cartesian
 B with the monoidal path-space ( 1 
our desired rule
 ). To get
 IdA B(f g) = (u:A) (v:A) (q:IdA(uv))IdB(f (u) g(v))
 we want a pullback in E op:
 1 
(A B) ( 1 A) ( 1 B)
 (A B) (A B) (( 1 A) B) (( 1 A) B)
Identity types of exponentials
 We want a pullback in E op:
 1 
(A B) ( 1 A) ( 1 B)
 (A B)2 (( 1 A) B)2
Identity types of exponentials
 By Yoneda, we want a pullback in Set for all X E op:
 E op(X 1 (A B)) E op X ( 1 A) ( 1 B)
 E op(X (A B)2) E op(X (( 1 A) B)2)
Identity types of exponentials
 Now we apply universal properties...
 E op(X 1 (A B)) E op X ( 1 A) ( 1 B)
 E op(X (A B)2) E op(X (( 1 A) B)2)
Identity types of exponentials
 Now we apply universal properties...
 E op( 1 XA B) E op X ( 1 A) ( 1 B)
 E op(X (A B)2) E op(X (( 1 A) B)2)
Identity types of exponentials
 Now we apply universal properties...
 E op( 1 XA B) E op X ( 1 A) ( 1 B)
 E op(X (A B)2) E op(X (( 1 A) B)2)
Identity types of exponentials
 Now we apply universal properties...
 E op(( 1 X) AB) E op X ( 1 A) ( 1 B)
 E op(X (A B)2) E op(X (( 1 A) B)2)
Identity types of exponentials
 Now we apply universal properties...
 E op(( 1 X) AB) E op X ( 1 A) ( 1 B)
 E op(X (A B)2) E op(X (( 1 A) B)2)
Identity types of exponentials
 Now we apply universal properties...
 E op(( 1 X) AB) E op X ( 1 A) ( 1 B)
 E op(2 XA B) E op(X (( 1 A) B)2)
Identity types of exponentials
 Now we apply universal properties...
 E op(( 1 X) AB) E op X ( 1 A) ( 1 B)
 E op(2 XA B) E op(X (( 1 A) B)2)
Identity types of exponentials
 Now we apply universal properties...
 E op(( 1 X) AB) E op X ( 1 A) ( 1 B)
 E op((2 X) AB) E op(X (( 1 A) B)2)
Identity types of exponentials
 Now we apply universal properties...
 E op(( 1 X) AB) E op X ( 1 A) ( 1 B)
 E op((2 X) AB) E op(X (( 1 A) B)2)
Identity types of exponentials
 Now we apply universal properties...
 E op(( 1 X) AB) E op X ( 1 A) 1 B
 E op((2 X) AB) E op(X (( 1 A) B)2)
Identity types of exponentials
 Now we apply universal properties...
 E op(( 1 X) AB) E op X ( 1 A) 1 B
 E op((2 X) AB) E op(X (( 1 A) B)2)
Identity types of exponentials
 Now we apply universal properties...
 E op(( 1 X) AB) E op 1 (X ( 1 A))B
 E op((2 X) AB) E op(X (( 1 A) B)2)
Identity types of exponentials
 Now we apply universal properties...
 E op(( 1 X) AB) E op 1 (X ( 1 A))B
 E op((2 X) AB) E op(X (( 1 A) B)2)
Identity types of exponentials
 Now we apply universal properties...
 E op(( 1 X) AB) E op 1 (X ( 1 A))B
 E op((2 X) AB) E op(2 X ( 1 A) B)
Identity types of exponentials
 Now we apply universal properties...
 E op(( 1 X) AB) E op 1 (X ( 1 A))B
 E op((2 X) AB) E op(2 X ( 1 A) B)
Identity types of exponentials
 Now we apply universal properties...
 E op(( 1 X) AB) E op 1 (X ( 1 A))B
 E op((2 X) AB) E op((2 X) ( 1 A)B)
Identity types of exponentials
 Now we apply universal properties...
 E op(( 1 X) AB) E op 1 (X ( 1 A))B
 E op((2 X) AB) E op((2 X) ( 1 A)B)
 And now, by Yoneda again...
Identity types of exponentials
 We equivalently want a pushout in E op:
 (2 X) ( 1 A) 1 (X ( 1 A))
 (2 X) A ( 1 X) A
Identity types of exponentials
 Which means a pushout in E for all n:
 ((2 X) ( 1 A))n ( 1 (X ( 1 A)))n
 ((2 X) A)n (( 1 X) A)n
Identity types of exponentials
 Which means a pushout in E for all n:
 ((2 X) ( 1 A))n ( 1 (X ( 1 A)))n
 (2 X)n An (( 1 X) A)n
Identity types of exponentials
 Which means a pushout in E for all n:
 ((2 X) ( 1 A))n ( 1 (X ( 1 A)))n
 2 (Xn An) (( 1 X) A)n
Identity types of exponentials
 Which means a pushout in E for all n:
 (2 X)n ( 1 A)n ( 1 (X ( 1 A)))n
 2 (Xn An) (( 1 X) A)n
Identity types of exponentials
 Which means a pushout in E for all n:
 2 (Xn An+1) ( 1 (X ( 1 A)))n
 2 (Xn An) (( 1 X) A)n
Identity types of exponentials
 Which means a pushout in E for all n:
 2 (Xn An+1) ( 1 (X ( 1 A)))n
 2 (Xn An) ( 1 X)n An
Identity types of exponentials
 Which means a pushout in E for all n:
 2 (Xn An+1) ( 1 (X ( 1 A)))n
 2 (Xn An) (2 Xn+n Xn 1) An
Identity types of exponentials
 Which means a pushout in E for all n:
 2 (Xn An+1) ( 1 (X ( 1 A)))n
 2 (Xn An) 2 (Xn An)+n (Xn 1 An)
Identity types of exponentials
 Which means a pushout in E for all n:
 2 (Xn An+1) ( 1 (X ( 1 A)))n
 2 (Xn An) 2 (Xn An)+n (Xn 1 An)
 ( 1 (X ( 1 A)))n
 =2 (X ( 1 A))n+n (X ( 1 A))n 1
 =2 (Xn ( 1 A)n)+n (Xn 1 ( 1 A)n 1)
 =2 (Xn An+1)+n (Xn 1 An)
Identity types of exponentials
 Which means a pushout in E for all n:
 2 (Xn An+1) 2 (Xn An+1)+n (Xn 1 An)
 2 (Xn An) 2 (Xn An)+n (Xn 1 An)
 ( 1 (X ( 1 A)))n
 =2 (X ( 1 A))n+n (X ( 1 A))n 1
 =2 (Xn ( 1 A)n)+n (Xn 1 ( 1 A)n 1)
 =2 (Xn An+1)+n (Xn 1 An)
Identity types of exponentials
 2 (Xn An+1) 2 (Xn An+1)+n (Xn 1 An)
 2 (Xn An) 2 (Xn An)+n (Xn 1 An)
 But this is just a coproduct of two pushout squares:
 2 (Xn An+1) 2 (Xn An+1)
 2 (Xn An) 2 (Xn An)
 n (Xn 1 An)
 n (Xn 1 An)
 Thus, it is a pushout, completing the proof of our desired rule
 IdA B(f g) = (u:A) (v:A) (q:IdA(uv))IdB(f (u) g(v))
 The same ideas work for dependent types and for-types.
Outline
 1 The magic of semicartesian cubes
 2 Paths in exponentials
 3 The parametricity universe
 4 The universe of brant types
 5 Cubical spaces
 6 Explaining the universe
Paths in the universe
 If U classi es small maps, then
 E op(X 1 U)=E op( 1 XU)
 so 1 U classi es small maps over cylinders.
 By extensivity , a map Y 
coproduct too:
 Yn
 =
 ( 1 X)decomposes Yn as a
 An +Bn + k nCnk
 ( 1 X)n Xn+Xn+ k nXn k
 =
Cubesovercylinders
 X2 X2
 X1
 X1
Cubesovercylinders
 X2 X2
 A2 B2
 X1
 X1
Cubesovercylinders
 X2 X2
 X1
 C20
 X1
Cubes over cylinders
 X2
 C21
 X1
 X1
 X2
Cubesovercylinders
 X2 X2
 X1
 C20
 X1
 C21 =
Cubesovercylinders
 X2 X2
 X1
 C20
 X1
 A1 B1
Cubical operators over cylinders
 Let 
(mn), so : n m
 +.
 An +Bn + k nCnk Am+Bm+ mCm
 Xn +Xn + k nXn k Xm+Xm+ mXm
 Any preserves the rst two summands, so we have
 AB E op with maps A X and B X.
 Sn 
(k) = 
(nn) permutes the summands Xn k , and its
 subgroup Sn k acts on Xn k . Thus, Cnk = Cnk k k.
 If 
m, then maps Xn k to Xm . These
 (k) 
assemble the Cnk into C E op with a map C X.
 If 
+, then maps Xn k to one of the rst Xm s.
 These assemble into maps C 
A and C B over X.
Cubical operators over cylinders
 Let 
(mn), so : n m
 +.
 An +Bn + k nCnk Am+Bm+ mCm
 Xn +Xn + k nXn k Xm+Xm+ mXm
 Any preserves the rst two summands, so we have
 AB E op with maps A X and B X.
 Sn 
(k) = 
(nn) permutes the summands Xn k , and its
 subgroup Sn k acts on Xn k . Thus, Cnk = Cnk k k.
 If 
m, then maps Xn k to Xm . These
 (k) 
assemble the Cnk into C E op with a map C X.
 If 
+, then maps Xn k to one of the rst Xm s.
 These assemble into maps C 
A and C B over X.
Cubical operators over cylinders
 Let 
(mn), so : n m
 +.
 An +Bn + k nCnk Am+Bm+ mCm
 Xn +Xn + k nXn k Xm+Xm+ mXm
 Any preserves the rst two summands, so we have
 AB E op with maps A X and B X.
 Sn 
(k) = 
(nn) permutes the summands Xn k , and its
 subgroup Sn k acts on Xn k . Thus, Cnk = Cnk k k.
 If 
m, then maps Xn k to Xm . These
 (k) 
assemble the Cnk into C E op with a map C X.
 If 
+, then maps Xn k to one of the rst Xm s.
 These assemble into maps C 
A and C B over X.
Cubical operators over cylinders
 Let 
(mn), so : n m
 +.
 An +Bn + k nCnk Am+Bm+ mCm
 Xn +Xn + k nXn k Xm+Xm+ mXm
 Any preserves the rst two summands, so we have
 AB E op with maps A X and B X.
 Sn 
(k) = 
(nn) permutes the summands Xn k , and its
 subgroup Sn k acts on Xn k . Thus, Cnk = Cnk k k.
 If 
m, then maps Xn k to Xm . These
 (k) 
assemble the Cnk into C E op with a map C X.
 If 
+, then maps Xn k to one of the rst Xm s.
 These assemble into maps C 
A and C B over X.
Typefamiliesovercylinders
 Thus, fromY ( 1 X),weextractaspaninE op X:
 A C B
 X
 Theorem
 ForX E op,wehaveanequivalenceofcategories
 E op ( 1 X) (E op X)( )
 (AlsogeneralizestomanyotherK replacing 1.)
Identitytypesof theparametricityuniverse
 Corollary
 ThereisaU0 E op thatclassi essmallmaps,andsuchthatthere
 isatrivial bration(i.e.amapwithRLPagainstmonos)
 ( 1 U0) (AB:U0)(A B U0)
 This isnotanisomorphism: theisomorphiccopiesCnkhavetobe
 classi edseparately.
Identitytypesof theparametricityuniverse
 Corollary
 ThereisaU0 E op thatclassi essmallmaps,andsuchthatthere
 isatrivial bration(i.e.amapwithRLPagainstmonos)
 ( 1 U0) (AB:U0)(A B U0)
 This isnotanisomorphism: theisomorphiccopiesCnkhavetobe
 classi edseparately.
 Trivial brationshavesections, soweinterpretasyntacticretraction
 (A B U0) IdU0(AB) (A B U0) p p
 Thus withU0modelsatheoryof internalparametricity,whose
 identitytypes consistofarbitrarycorrespondences.
Outline
 1 The magic of semicartesian cubes
 2 Paths in exponentials
 3 The parametricity universe
 4 The universe of brant types
 5 Cubical spaces
 6 Explaining the universe
Towards a universe of brant types
 Wed like to de ne U to be
 the subtype of U0 whose identity type
 correspondences are one-to-one.
 For any span A C B, i.e. correspondence C : A B U0,
 we have the type of assertions that it is one-to-one:
 is11(C) :
 (a:A)isContr( (b:B)C(ab))
 (b:B)isContr( (a:A)C(ab))
 If ABC lie in a slice E op X, so does is11(C) E op X.
The universal correspondence
 We pull back the universal type family along the adjunction counit:
 1 
U0
 ( 1 U0) U0
 This yields a type family over the cylinder 1 ( 1 U0), hence a
 universal correspondence over 1 U0:
 A0 C0 B0
 1 
U0
 Thus we have the classifying object is11(C0) E op ( 1 U0).
 BUT: this is a predicate on 1 U0, not U0 itself.
A rst-order approximation
 We can x this with the berwise amazing right adjoint:
 U1 =
 Theorem
 is11(C0)U0
 The classifying map 
U0 of a type family 
P : U0 lifts to U1
 if and only if the correspondence Id P is one-to-one.
 P : U0 lifts to U1
 if and only if the correspondence Id P is one-to-one.
A rst-order approximation
 We can x this with the berwise amazing right adjoint:
 U1 =
 Theorem
 is11(C0)U0
 The classifying map 
U0 of a type family 
P : U0 lifts to U1
 if and only if the correspondence Id P is one-to-one.
 BUT: This correspondence is still U0-valued: even for 
Id P :P[ ] P[ ] U0
 So we cant consistently use U1 as the universe.
 P : U1,
A second-order approximation
 For any A C B wehave a type classif(CU1) of U1-valued
 classifying maps for C, i.e. pullback squares
 C U1
 A B U1
 Then we de ne a further improved universe:
 U2 =
 The identity types of 
is11(C1) classif(C1U1)U1
 P : U2 are one-to-one and U1-valued.
A limit construction
 We continue inductively and take a limit:
 Un+1 = 
is11(Cn) classif(CnUn)Un
 U =lim n
 (
 Theorem
 Un 
U1 U0)
 The identity types of 
P : U are one-to-one and U-valued.
 U classi es maps with contractible spaces of uniform Kan llers.
Higher coinduction for IdU
 .
 U is a higher coinductive type: the terminal coalgebra of a functor
 involving 
Its higher destructors assemble into
 : IdU(AB) 1-1-Corr(AB)
 The magic cylinder formula implies a formula for paths in 
Thus, IdU is also a higher coinductive type.
 By higher coinduction (univ. prop. of lim and 
: 1-1-Corr(AB) 
such that p
 Even if 
p.
 for U0 were an isomorphism, this wouldnt be:
 IdU contains more data than 1-1-Corr.
 .
 ) we de ne
 IdU(AB)
Fibrancy of type-formers
 We lift all the type-formers from U0 to U by higher coinduction.
 E.g. for-types:
 (A:U)(A 
(A:U0)(A 
We must show that:
 U) U
 0
 U0) U0
 takes identi cations to one-to-one correspondences.
 These correspondences are isomorphic to some-type.
Strictifying identity types
 This amounts to specifying the computation rules for ap and Id :
 apXY (x:X)Y(x)(A2B2) (IdA2B2
 XY (x:X)Y(x)
 Id
 (x:A)B(s t) 
)
 (q:Id A( 1s 1t))Id q
 (
 x:A)B( 2s 2t)
 such that the latter equality holds up to isomorphism for powers
 ( 1 ) inE op.
 This works because the identity types of a-type are another-type (and similarly for all other type-formers).
 This is the coherence theorem strictifying Id = to a
 de nitional equality.
Conclusion: cubicaluniverses
 Theorem-in-progress
 H.O.T.T.hasamodel inE op, foranypresheaf toposE.
 Inparticular, ithasamodel in .
 Conjecture
 Bygluingwithaglobal-sectionsornervefunctorvaluedin or
 presheavesthereof,wecanprovecanonicityandnormalization.
 Notethat
 1Wemusthavesymmetryin , tointerpret Id andIdU.
 2Wemusthavesymmetryinsyntax, forthenervetoliein .
Outline
 1 The magic of semicartesian cubes
 2 Paths in exponentials
 3 The parametricity universe
 4 The universe of brant types
 5 Cubical spaces
 6 Explaining the universe
Towards higher topos models
 Symmetry solves syntactic problems, but creates semantic ones:
 The syntax-like model in doesnt present classical homotopy.
 There could be an equivariant version. But theres another way.
 Two approaches to de ning higher homotopical structures:
 1 As diagrams of sets
 E.g. quasicategories
 More parsimonious
 2 As diagrams of spaces
 E.g. complete Segal spaces
 Often better-behaved
Cubical spaces
 LetEbeatype-theoreticmodelpresheaftopos,e.g.:
 E=sSet, simplicial sets,withtheKanmodel structure
 (presentsthehomotopytheoryofspaces).
 E=simplicialpresheaves,withaleftexact localizationofthe
 injectivemodel structure(presentsan( 1)-topos).
 Theorem(cf.RezkSchwede Shipleyforthesimplicialversion)
 Theinjectivemodel structureonE op admitsaleftBous eld
 localization,calledtherealizationmodel structure, suchthat:
 1 It isQuillenequivalenttoE.
 2 It isalsoatype-theoreticmodel topos.
 (Thoughnotaleftexact localizationoftheinjectiveone.)
Theuniverseof realization brations
 Theorem
 IfU0rlz classi esrealization brations,andUrlz=limnUnrlzas
 before, thereisatrivial bration
 ( 1 Urlz) (AB:Urlz)1-1-Corr(AB)
 Corollary
 Therealizationmodel structureinterpretsallofH.O.T.T.
 Thus,H.O.T.T.hasmodels inallGrothendieck( 1)-toposes.
Why IdU has no-rule
 1 IdU0(AB) is not isomorphic to A B U0.
 2 IdU contains higher destructors in addition to 1-1-Corr.
 3 Injective bration structures over a cylinder contain more data
 than those on a span.
 4 Homotopical constancy structures over a cylinder contain more
 data than those on a span.
 5 Syntactically, IdU must contain additional sym data.
Outline
 1 The magic of semicartesian cubes
 2 Paths in exponentials
 3 The parametricity universe
 4 The universe of brant types
 5 Cubical spaces
 6 Explaining the universe
What kind of type is the universe?
 Traditionally, the universe is thought of (informally) as inductively
 de ned, with constructors 
, and Tarski eliminator El
 de ned by recursion.
 Not true internally, but informs meaning explanations and
 inductive-recursive universe constructions.
 An observational Id would also be de ned by recursion over
 these constructors, with clauses for Id , Id , etc.
 But:
 Its hard (not impossible) to make an inductively de ned
 universe univalent.
 Suggests a closed universe, which has to be rede ned whenever
 we add new type formers.
Co-meaning explanations
 We instead consider U (still informally) to be coinductively de ned.
 Now El and Id are destructors.
 Each type former , , ...is de ned by corecursion, specifying
 its elements, and its identity types of the same class .
 E.g. 
is a corecursive function
 (A:U)(A 
U)
 which makes sense because Id is another-type.
 U,
 Explains an open universe: can introduce new type formers
 without rede ning U, just applying its corecursion principle.
 The semantic universe of brant types is higher coinductive.
 This gives a philosophical reason for the coinductive behavior of
 IdU, having but no .
Back to Bishop
 Recall Bishops dicta:
 A set is de ned by describing exactly what must be
 done in order to construct an element of the set and what
 must be done in order to show that two elements are equal.
 An operation f from A into B is called a function if
 whenever aa A and a =a, we have f(a) = f(a).
Coinductive synthetic-groupoids
 Under propositions-as-types, this naturally becomes coinductive:
 A type is de ned by describing exactly what must be
 done in order to construct an element of the type and
 de ning a type of ways to identify any two such elements.
 An operation f from A into B is called a function if for
 aa :A we have a function from a = a to f(a) = f(a).
Coinductive synthetic-groupoids
 Under propositions-as-types, this naturally becomes coinductive:
 A type is de ned by describing exactly what must be
 done in order to construct an element of the type and
 de ning a type of ways to identify any two such elements.
 An operation f from A into B is called a function if for
 aa :A we have a function from a = a to f(a) = f(a).
 If we augment it with a bit of univalence:
 We de ne a type U whose elements are types, where
 two types are identi ed by a one-to-one correspondence.
 Every element of every type is identi ed with itself. For
 a type A : U, this yields its own type of identi cations.
 We get a philosophical vision that leads ineluctably to H.O.T.T.,
 as a theory of coinductive-groupoids




















Under consideration for publication in Theory and Practice of Logic Programming
 1
 (Co)recursion in Logic Programming: Lazy vs Eager∗
 arXiv:1402.3690v4  [cs.PL]  20 May 2014
 J ´ ONATHAN HERAS
 School of Computing, University of Dundee, UK
 (e-mail: jonathanheras@computing.dundee.ac.uk)
 EKATERINAKOMENDANTSKAYA
 School of Computing, University of Dundee, UK
 (e-mail: katya@computing.dundee.ac.uk)
 MARTINSCHMIDT
 Institute of Cognitive Science, University of Osnabr¨uck, Germany
 (e-mail: martisch@uos.de)
 submitted 1 January 2003; revised 1 January 2003; accepted 1 January 2003
 Abstract
 CoAlgebraic Logic Programming (CoALP) is a dialect of Logic Programming designed to bring a more
 precise compile-time and run-time analysis of termination and productivity for recursive and corecursive
 functions in Logic Programming. Its second goal is to introduce guarded lazy (co)recursion akin to func
tional theorem provers into logic programming. In this paper, we explain lazy features of CoALP, and
 compare them with the loop-analysis and eager execution in Coinductive Logic Programming (CoLP). We
 conclude by outlining the future directions in developing the guarded (co)recursion in logic programming.
 KEYWORDS:Logic Programming, Recursion, Corecursion, Termination, Productivity, Guardedness.
 1 Introduction
 Logic Programming (LP) was conceived as a recursive programming language for first-order
 logic. Prolog and various other implementations of LP feature eager derivations, and therefore
 termination has been central for logic programming (de Schreye and Decorte 1994). However,
 unlike e.g. functional languages, LP has not developed an operational semantics supporting ex
plicit analysis of termination. In typed programming languages like Coq or Agda, it is possible
 to introduce syntactic (static) checks that ensure structural recursion, and hence termination of
 programs at run-time. In Prolog, there is no support of this kind.
 Example 1.1 (BitList) Consider the following recursive program that defines lists of bits.
 1.bit(0) ←
 2.bit(1) ←
 3.bitlist([]) ←
 4.bitlist([X|Y]) ← bit(X),bitlist(Y)
 ∗ The work of the first two authors was supported by EPSRC Grant EP/K031864/1.
2
 J. Heras, E. Komendantskaya, and M. Schmidt
 76
 01
 Terminating
 54
 23
 ▲▲▲▲▲
 76
 01
 Non-terminating
 Recursion
 54
 23
 76
 01
 Productive
 54
 23
 ▲▲▲▲▲
 76
 01
 Non-productive
 Corecursion
 Fig. 1. Distinguishing well-founded and non-well-founded cases of recursion and corecursion.
 54
 23
 It is a terminating program, however, if the order of clauses (3) and (4), or the order of atoms in
 clause (4) is accidentally swapped, the program would run into an infinite loop.
 This example illustrates that non-terminating (co)recursion is distinguished only empirically
 at run-time in LP. This distinction is not always accurate, and may depend on searching strategies
 of the compiler, rather than semantic meaning of the program.
 Coinductive Logic Programming (CoLP) (Gupta et al. 2007; Simon et al. 2007) has been in
troduced as a means of supporting corecursion in LP. A representative example of coinductive
 programmingis to reason about an infinite data structure, for example an infinite stream of bits.
 Example 1.2 (BitStream) Given the definition of bits as in Example 1.1, an infinite stream of
 bits is defined as:
 1.stream([X|Y]) ← bit(X),stream(Y)
 Note that unlike BitList, we no longer have the base case for recursion on stream.
 The tradition (Coquand 1994) has a dual notion to termination for well-behaving corecur
sion– and that is productivity. If termination imposes the condition that any call to an induc
tively defined predicate like bit must terminate, then productivity requires that every call to a
 coinductive predicate like stream must produce some partially observed structure in a finite
 number of steps. E.g. calling stream(X)?,the program must compute an answer [0|Y] observ
ing the component 0 in finite time. Moreover, the productivity imposes a second condition: the
 computation must be able to proceed corecursively, e.g. in our example, the condition is for Y
 to be an infinite productive datastructure. This situation is explained in e.g. (Abel et al. 2013;
 Bertot and Komendantskaya 2008).
 CoLP deals with programs like BitStream by using a combination of eager evaluation, SLD
resolution and loop analysis. In simplified terms, for a goalstream(X)?the resolventloop detec
tion would allow to return an answer X=[0|X]; by observing the “regular” pattern in resolvents
 involving Clause (1) in the derivations. Similarly to standard (recursive) LP, non-terminating
 cases of corecursion (where no regular loop can be found) are not formally analysed in CoLP.
 Example 1.3 (BadStream) BadStream is not productive; that is, it would be executed infinitely
 without actually constructing a stream:
 1.badstream([X|Y]) ← badstream([X|Y])
 Adifferent case of corecursion is the below example, which is productive, but cannot be han
dled by CoLP loop detector, as the stream it defines is not regular.
 Example 1.4 (TakeFirstN) The program TakeFirstN defines the stream of natural numbers,
(Co)recursion in Logic Programming: Lazy vs Eager
 and allows to construct a list with the first n elements of the stream by calling taken.
 1.from(X,[X|Y]) ← from(s(X),Y)
 2.take(0,Y,[]) ←
 3.take(s(X),[Y|Z],[Y|R]) ← take(X,Z,R)
 4.taken(N,X) ← from(0,Y),take(N,Y,X)
 3
 In CoLP, calls to e.g. taken(s(s(0)),X)?fall into infinite computationsthat are not handled
 by the loop detection procedure. Similar to how LP would be unable to handle BitList with
 swapped atoms in clause (4) though in principle the program describes a well-founded inductive
 structure, CoLP would not be able to handle TakeFirstN although it is a perfectly productive
 stream. For the query taken, it is intuitively clear that, the construction of the first n elements of
 the stream should take a finite number of derivation steps.
 CoalgebraicLogicProgramming(CoALP)(Komendantskaya and Power 2011;Komendantskaya et al. 2014a)
 gives a new (coalgebraic) operational semantics for LP; and in particular it offers new methods
 to analyse termination and productivity of logic programs. Using CoALP, we present here a
 coherent operational treatment of recursion and corecursion in LP, and discuss new methods
 to distinguish well-founded and non-well-founded cases of (co)recursion in LP, as outlined in
 Figure 1. Unlike Prolog or CoLP, CoALP is a first lazy dialect of logic programming; and it fea
tures guarded (co)recursion akin to structural recursion and guarded corecursion in e.g. Coq or
 Agda (Coquand 1994; Abel et al. 2013). The current implementation of CoALP in parallel lan
guage Go is available in (Komendantskaya et al. 2014b); and is tested on a few benchmarks in
 this paper. Here, weabstract fromsomeofthetechnicaldetailsavailable in (Komendantskaya et al. 2014a)
 and from implementation details available in (Komendantskaya et al. 2014c) and give a higher
level discussion of the issues of termination and productivity in LP.
 The rest of the paper is structured as follows. In Section 2, we explain the role of laziness in
 semantics and implementation of CoALP; in Section 3, we discuss the effect of guarded corecur
sion. Section 4 is devoted to discussion of our current work on soundness properties for corecur
sive logic programming.
 2 LazyCorecursion in Logic Programming
 CoALP uses the standard syntax of Horn-clause logic programming (Lloyd 1987), but offers a
 newderivation algorithm in place of the SLD-resolution. One of the main distinguishing features
 of CoALPis its laziness. To our knowledge, it is the first lazy dialect of logic programming. The
 issue is best explained using the following example:
 Example 2.1 Given the program BitList and the query bitlist([X|Y]), the standard algo
rithm of SLD-resolution (Lloyd 1987) will eagerly attempt to find a derivation, e.g.:
 bitlist([X|Y])−→bit(X),bitlist(Y) X=0
 −→bitlist(Y)Y=[]
 −→✷
 For the program BitStream this will give rise to an infinite SLD-derivation:
 stream([X|Y])−→bit(X),stream(Y) X=0
 −→stream(Y)Y=[X1|Y1]
 −→ stream([X1|Y1])...
 In the above setting, there is no natural place for laziness, as ultimately the strong side of the
 procedure is a fully automated proof search. Fibrational coalgebraic operational semantics of LP
4
 J. Heras, E. Komendantskaya, and M. Schmidt
 θ1
 →
 1. stream(X)
 3. bitlist(X)
 θ2
 →... θ3
 →
 stream([X1|Y])
 bit(X1)
 stream(Y)
 2. bitlist(X)
 θ1
 1
 →
 stream([0|[X1|Y2]])
 bit(0)
 ✷
 stream([X1|Y2])
 bit(X1)
 bitlist([])
 ✷
 θ2
 1
 →
 θ2
 2
 →... θ2
 3
 bitlist([X1|Y])
 bit(X1)
 list(Y)
 →
 bit(0)
 ✷
 stream(Y2)
 bitlist([0|[]])
 →... →∞
 bitlist([])
 ✷
 Fig. 2. 1: Three coinductive trees representing a coinductive derivation for the goal G = stream(X) and the program
 BitStream, with θ1 = X/[X1|Y], θ2 = X1/0 and θ3 = Y/[X1|Y2]. 2-3: Coinductive trees representing two coinductive
 derivations for the goal G = bitlist(X) and the program BitList, with θ1
 1 = X/[], θ2
 1 = X/[X1|Y], θ2
 2 = X1/0, and
 θ2
 3 = Y/[].
 presented in (Komendantskaya et al. 2014a) inspired us to introduce a structure which we call
 coinductive tree; we use it as a measure for the size of lazy steps in derivations:
 Definition 2.1 Let P be a logic program and G =← A be an atomic goal. The coinductive tree
 for A is a (possibly infinite) tree T satisfying the following properties.
 • Aisthe root of T.
 • Eachnodein T iseither an and-node(labelled by an atom) or an or-node (labelled by “•”). The
 root of the tree is an and-node.
 • For every and-node A′ occurring in T, if there exist exactly m > 0 distinct clauses C1,...,Cm in
 P (a clause Ci has the form Bi ← Bi
 1,...,Bi ni
 , for some ni), such that A′ = B1θ1 = ... = Bmθm,
 for mgus θ1,...,θm, then A′ has exactly m children given by or-nodes, such that, for every i ∈
 {1,...,m}, the ith or-node has ni children given by and-nodes Bi
 1θi,...,Bi ni
 θi.
 In such a case, we sayCi and θi are internal resolvents of A′.
 Coinductivetrees resemble an-orparallel trees (Gupta and Costa 1994),see (Komendantskaya et al. 2014a;
 Komendantskaya et al. 2014c) for discussion of their parallel features. However, they restrict
 mgus used to form nodes to term-matching. Given two first order atomic formulae A and B, an
 mgu θ for A and B is called a term-matcher if A = Bθ. In Definition 2.1, note the condition
 A′ =B1θ1 =...=Bmθm.
 Example 2.2 Figure 2shows coinductivetrees for various goals in BitStream and BitList; com
pare with SLD-derivations in Example 2.1. Note that each of those trees is finite by construction
 of Definition 2.1; and we do not impose any additional conditions. The size of coinductive trees
 varies, but it is automatically determined by construction of the definition.
 Wenowdefinederivations between coinductive trees– a lazy analogue of SLD-derivations.
 Definition 2.2 Let G = A,T be a goal given by an atom ← A and the coinductive tree T
(Co)recursion in Logic Programming: Lazy vs Eager
 5
 induced by A, and let C be a clause H ← B1,...,Bn. Then, the goal G′ is coinductively derived
 from G andC using the mgu θ if the following conditions hold:
 ⋆ Q(¯ t) is a node in T.
 ⋆⋆ θisanmguofQ(¯ t) andH.
 ⋆⋆⋆ G′ isgivenbythe(coinductive) tree Tθ with the root Aθ.
 Definition 2.3 AcoinductivederivationofP∪{G}consistsofasequenceofgoalsG=G0,G1,...
 and a sequence θ1,θ2,... of mgus such that each Gi+1 is derived from a node A ∈ Ti (where Ti
 is the coinductive tree of Gi) and a clause C using a non-empty substitution θi+1. In this case,
 A,C,θi+1 is called a resolvent.
 Coinductive derivations resemble tree rewriting. They produce the “lazy” corecursive effect:
 derivations are given by potentially infinite number of steps, where each individual step is exe
cuted in finite time.
 Example 2.3 Figure 2 shows three possible coinductive derivations for BitStream and BitList.
 Note that two derivations for BitList terminate (with ✷ closing all branches). Note also, that
 this time, due to the and-or parallel nature of coinductive treees, changing the order of atoms or
 clauses in the program BitList will not change the result.
 For terminating coinductive derivations, we require at least one or-subtree of the coinductive
 tree to be closed (with ✷ leaves). We also say in such cases that the coinductive tree contains
 a success subtree. The last coinductive trees in the second and third derivation of Figure 2 are
 themselves success subtrees.
 Due to its and-or parallel properties (Komendantskaya et al. 2014c), CoALP is more robust
 than eager sequential SLD-resolution when it comes to reflecting program's operational mean
ing; and mere change in the clause order would not place a terminating recursive function into
 a non-terminating class, cf. Figure 1. Yet more importantly, this new coinductive derivation pro
cedure allows us to characterise productive and non-productive programs with better precision.
 In Introduction, we have seen that according to eager interpreter of CoLP, both programs Bad
Stream and TakeFirstN are non-terminating; despite of one being productive, and another
non-productive. Next example shows that under lazy execution, productive programs with irreg
ular pattern of resolvents can be handled more naturally.
 Example 2.4 Figure 3 shows the first steps in the derivation for the program TakeFirstN and
 the goal taken(s(s(0)),X). Unlike CoLP, CoALP is able to compute the second element of
 the stream in finite time.
 There will be classes of non-terminating and non-productive programs for which coinductive
 trees grow infinite, and lazy derivations fail being ”lazy”. The program BadStream is one such
 example. We will consider this issue in the next section.
 3 Guarding (Co)recursion
 The previous section introduced coinductive trees, which allowed us to distinguish terminating
 and productive programs like BitStream, BitList, TakeFirstN from non-productive programs
 like BadStream, by simply observing that coinductive trees remain finite for the former, while
6
 J. Heras, E. Komendantskaya, and M. Schmidt
 θ2
 −→
 taken(s2(0),[X1,X2|R2])
 θ1
 −→
 taken(s2(0),X)
 taken(s2(0),[X1|R1])
 from(0,[X1|Y1])
 from(0,[X1, X2|Y2])
 take(s2(0),[X1|Y1],[X1|R1])
 from(0,Y)
 take(s2(0),Y,X)
 →
 take(s(0),Y1,R1)
 →
 take(s2(0),[X1,X2|Y2],[X1,X2|R2])
 take(s(0),[X2|Y2],[X2|R2])
 take(0,Y2,R2)
 Fig. 3. First steps of the derivation for the goal taken(s2(0),X)– s2(0) denotes s(s(0))– and the program
 TakeFirstN, with θ1 = Y/[X1|Y1],X/[X1|R1] and θ2 = Y1/[X2|Y2],R1/[X2|R2]. As take is an inductive predicate, and
 from is coinductive; resolvents for take nodes are given priority.
 connected(O,Z)
 edge(O,Y)
 connected(Y,Z)
 edge(Y,Y1)
 connected(Y1,Z)
 edge(Y1,Y2)
 connected(Y2,Z)
 .
 .
 .
 Fig. 4. The infinite coinductive tree for the program GC from from Example 3.1, for the database edge(0,1) ←.
 growinginfinite for the latter. It was especially significant that this new approachwas, unlike Pro
log, robust to permutations of clauses and atoms, and, unlike CoLP, was working with productive
 irregular streams. Curiously, the following logic programfails to producefinite coinductive trees:
 Example 3.1 (GC) Let GC (for graph connectivity) denote the logic program
 1.connected(X,X) ←
 2.connected(X,Y) ← edge(X,Z),connected(Z,Y)
 It would be used with database of graph edges, like edge(0,1)←.
 The programgives rise to infinite coinductive trees, see Figure 4. It would terminate in LP, but,
 similarly to our discussion of BitList, would lose the termination property if the order of clauses
 (1) and (2) changes, or if the order of the atoms in clause (2) changes.
 Thereasonbehindinfinityofcoinductivetreesfor the aboveprogramis the absenceoffunction
 symbols– “constructors” in the clause heads. The lazy nature of coinductive trees was in part
 due to the term-matching used to compute them. Term-matching loses its restrictive power in the
 absence of constructors. A very similar procedure of guarding recursion by constructors of types
 is used in e.g. Coq or Agda. This observation would suggest an easy way to fix the GC example,
 by introducing reducing dummy-constructors:
 Example 3.2 (Guarded GC)
 1.connected(X,cons(Y,Z)) ← edge(X,Y),connected(Y,Z)
 2.connected(X,nil) ←
(Co)recursion in Logic Programming: Lazy vs Eager
 7
 Considerations of this kind led us to believe that our lazy (co)recursive approach opens the
 way for a compile-time termination and productivity checks akin to respective checks in Coq or
 Agda (Coquand 1994; Abel et al. 2013). The programmer would be warned of non-terminating
 cases and asked to find a guarded reformulation for his functions. In Coq and Agda, different
 checks are imposed on recursive functions (“structural recursion” condition) and corecursive
 functions (“guardedness” checks). In logic programming terms, where types or predicate an
notations are unavailable, we can formulate a uniform productivity property for recursive and
 corecursive programs, as follows:
 Definition 3.1 Let P be a logic program, P is productive if for any goal G, the coinductive tree
 for P∪{G} has a finite size.
 The above is a semantic property; syntactically, we need to introduce guardedness checks
 to ensure productivity. The intuitive idea is to ensure that every coinductive program behaves
 like BitStream:BitStream is guarded by the coinductive function symbol (or “guard”) scons
 (denotedby [.|.]);and henceall coinductivetrees for it are finite, see Figure 2. On the contrary,
 Comember lacks a guarding constructor.
 Example 3.3 (Comember) The predicate comember is true if and only if the element X occurs
 an infinite number of times in the stream S.
 1.drop(H,[H|T],T) ←
 2.drop(H,[H1|T],T1) ← drop(H,T,T1)
 3.comember(X,S) ← drop(X,S,S1),comember(X,S1)
 Comemberisun-productivefor e.g.thecoinductivetree arising from the querycomember(X,S)
 contains a chain of alternating •'s and atoms comember(X,S1), comember(X,S2), etcetera,
 yielding an infinite coinductive tree.
 We will give a high-level formulation of guardedness checks here, for more technical discus
sion, see (Komendantskaya et al. 2014a).
 Guardedness Check 1 (GC1): If the same predicate Q occurs in the head and in the body of
 a clause, then there must exist a function symbol f occurring among the arguments of Q; such
 that the number of its occurrences is reduced from head to body.
 Example 3.4 (Guarded Comember) We propose the following guarded definition of comem
ber, thereby simplifying it and reducing an extra argument to drop.
 1.drop(H,[H|T]) ←
 2.drop(X,[H|T]) ← drop(X,T)
 3.gcomember(X,[H|T]) ← drop(X,[H|T]),gcomember(X,T)
 In CoALP, the goal gcomember(0,nats)will lazily search for 0 in an infinite stream of natural
 numbers, but it never falls into un-productive coinductive trees, as CoLP would do.
 GC1wouldbesufficientforsomeprograms,likeBitStream,wherethereisonlyone(co)inductive
 clause; but not in the general case. LP in general is not compositional, that is, composing two
 programs may yield a program that has semantic properties not present in the initial programs.
8
 J. Heras, E. Komendantskaya, and M. Schmidt
 stream2’([s(0)|Y],[s(Y1)|Z1])
 nat(0)
 ✷
 θ1
 −→... θ2
 −→
 stream2’([s(X)|Y],Z)
 nat(X)
 stream-aux([s(X)|Y],Z)
 →
 stream-aux([s(0)|Y],[s(Y1)|Z1])
 nat(Y1)
 stream2’([s(0)|Y],[s(Y1)|Z1])
 nat(0)
 ✷
 .
 .
 .
 Fig. 5. Coinductive derivation of stream2’([s(X)|Y],Z)and the program from Example 3.5 producing an infinite coinductive tree,
 with θ1 =X/0andθ2 =Z/[s(Y1)|Z1].ThefigurealsorepresentsoneGC-derivation generated duringGC3.GC3 detectsthe un-guarded
 loop; see the underlined atoms.
 Same rule applies in CoALP: if both P1 and P2 are productive programs, their composition is not
 guaranteed to be a productive program; the next check is imposed to cover the compositional
 cases.
 Guardedness Check 2 (GC2): For every clause head A, construct a coinductive tree with the
 root A. If there are atoms Q(¯ t) and Q(¯ t′) in the coinductive tree such that Q(¯ t′) is a child of Q(¯ t),
 apply GC1 to the clause Q(¯ t) ← Q(¯ t′).
 GC1–GC2handle some programs well, but they are still insufficient in the general case. The
 following program passes the checks GC1-GC2, but is not productive in the sense of Defini
tion 3.1, see Figure 5.
 Example 3.5 (Un-productive Program that passes GC1-GC2)
 1.stream2’([s(X)|Y],Z) ← nat(X), stream-aux([s(X)|Y],Z)
 2.stream-aux(X,[s(Y)|Z]) ← nat(Y), stream2’(X,[s(Y)|Z])
 Guardedness Check 3 (GC3): For every clause head A, start a coinductive derivation with
 the goal A imposing GC2 condition to every coinductive tree in the derivation, and imposing the
 following termination conditions:
 1. Terminate coinductive derivation if GC2 fails for at least one tree.
 2. Terminatecoinductivederivationif all branchesare eitherclosed with ✷ or containguarded
 loops only.
 Note that the checks GC1-GC3 we have introduced here are a pre-processing (compile
time) mechanism of CoALP. Once the program passed the guardedness checks, it does coin
ductive derivations lazily; and does not require any loop-detection procedures at run-time. If a
 program fails GC1-GC3, the programmer will be asked to re-formulate the definitions as we
 have seen in Examples 3.2 and 3.4. The first implementation of guardedness checks is available
 at (Komendantskaya et al. 2014b).
 We finish this section with Table 1 comparing how SWI-Prolog, CoLP and CoALP handle
 variousrecursive and corecursiveprograms.For CoALP,we also benchmarkguardednesschecks.
 For coinductive programs, CoLP can only handle coinductive programs that contain a regular
 pattern and fails otherwise (cf. Table 1); on the contrary, CoALP, in its lazy style, works for
 any productive program. This is illustrated, for instance, with the programs TakeFirstN and
 TakeRepeat. Table 1 shows that CoALP is slower than the CoLP interpreter and SWI-Prolog
(Co)recursion in Logic Programming: Lazy vs Eager
 CoALP
 GCtime: 0.0002s
 TakeFirstN†
 Takerepeat†
 Comember†
 GComember†
 SumFirstn†
 FibStream†
 Infinite Automata†
 Knights
 Finite Automata
 Ackermann
 Yes
 Yes
 Yes
 Yes
 Yes
 Yes
 Yes
 Yes
 Yes
 runtime: lazy execution
 GCtime: 0.0009s
 runtime: lazy execution
 Not guarded
 GCtime: 0.0011s
 runtime: lazy execution
 GCtime: 0.0013s
 runtime: lazy execution
 GCtime: 0.0006s
 runtime: lazy execution
 GCtime: 0.0011s
 runtime: lazy execution
 GCtime: 0.225s
 runtime: 3.002s
 GCtime: 0.0011s
 runtime: 0.0023s
 GCtime: 0.001s
 runtime: 13.23s
 CoLP
 No
 Yes (0.0001s)
 Yes? (0.0001s)
 Yes? (0.0001s)
 No
 No
 Yes (0.0001s)
 Yes (1.13s)
 Yes (0.04s)
 Yes (7.692s)
 SWI-Prolog
 No
 No
 No
 No
 No
 No
 No
 Yes (0.012s)
 Yes (0.0005s)
 Yes (3.192s)
 9
 Table 1. Execution of different programs in CoALP, CoLP and SWI-Prolog. Examples marked with † involve both
 inductive and coinductive predicates. In the table, “No” means that the system runs forever without returning an answer,
 and “Yes?” indicates that the program succeeds if it contains a regular pattern and fails otherwise.
 note that SWI-Prolog is a fully-tuned mature programming language and the CoLP interpreter
 runs on top of SWI-Prolog, as opposed to our implementation of CoALP in Go from scratch.
 4 Work-in-Progress: Soundness for Corecursion
 There are two main directions for CoALP's development, both related to soundness:
 (I) We are in the process of establishing soundness of GC1-GC3 that is, the property that, if a
 program P is guarded by GC1-GC3, then it is productive in CoALP.
 Proving this property in the general case is a challenge; and involves pattern analysis on re
solvents and also a proof of termination of GC1-GC3. Example 3.5 and Figure 5 give a flavor
 of the complicated cases the guardedness checks need to cover. Note that GC1-GC3 provide the
 guarding property only in the CoALP setting, and the same idea of guarding (co)recursion by
 constructors would fail for standard LP or CoLP, as many examples of this paper show.
 (II) Soundness of coinductive derivations needs to be established. This challenge is best illus
trated by the following example.
 Example 4.1 (Soundness for Comember) To check the validity of a query in Comember (Ex
ample 3.3) for an arbitrary stream, one needs to satisfy two conditions: 1) finding an element to
 dropin afinitetime, 2) findingguaranteesthat this finite computationwill be repeated an infinite
 numberof times for the given stream. CoLP would handlesuch a case for all streams that consist
 of a regular finite repeating pattern and will not be able to handle cases when the input stream
 is not regular. CoLP would fail to derive true or falsity of e.g. the query comember(0,nats),
 where nats is the stream of natural numbers, as CoLP falls into an infinite non-terminating
 computation and fails to produce any response to the query. CoALP in its current implemen
tation will handle any case of corecursion, including comember(0,nats), but in its lazy, and
 therefore partial, style.
10
 J. Heras, E. Komendantskaya, and M. Schmidt
 Similarly, TakeFirstN falls into an infinite loop with CoLP, but unfolds lazily with CoALP,
 see Figure 3. Laziness on its own, however, does not guarantee soundness.
 For inductive programs and recursive functions, CoALP yields the same theorems of sound
ness and completeness as classical LP (Lloyd 1987); cf. (Komendantskaya et al. 2014a). The
 only adaptation to the already described coindutive derivation procedure is the requirement that
 the derivation terminates and gives an answer whenever a success subtree is found. Thus, gener
alisation of standard soundness and completeness for induction in CoALP is not very surprising.
 Soundness of CoALP for coinductive programs is conceptually more interesting: it has to
 include a number of guarantees that need to be checked at compile-time and run-time, that is:
 1. Identification of the guarding pattern coming from sound guardedness checks;
 2. Guaranteethat the guardingpattern will be producedin a finite numberof derivation steps;
 3. Guarantee that the guarding pattern will be re-produced an infinite number of times.
 Item 3. in particular may allow for a few different solutions. In its basic form, it can be a
 repeated regular pattern, as it is done in CoLP. In a more sophisticated form, it can cover ir
regular patterns, as long as more involved guarantees of infinite execution are be provided, cf.
 Example 1.4 and Figure 3.
 To conclude, we have described a new methodto analyse termination and productivityof logic
 programsby meansof lazyguardedcorecursionin CoALP, as outlinedin Figure1. We advocated
 a new style of programming in LP, where the programmer is in charge of providing termination
 or productivity measures for (co)recursive programs at compile-time, as it is done in some other
 declarative languages with recursion and corecursion. Finally, we outlined the main directions
 towards establishing soundness results for CoALP outputs.
 References
 ABEL, A. ET AL. 2013. Copatterns: programming infinite structures by observations. In POPL'13. ACM
 SIGPLANNotices, vol. 48. 27–38.
 BERTOT, Y. AND KOMENDANTSKAYA, E. 2008. Inductive and coinductive components of corecursive
 functions in Coq. ENTSC 203, 5, 25–47.
 COQUAND, T. 1994. Infinite objects in type theory. In TYPES'93. LNCS, vol. 806. 62–78.
 DE SCHREYE, D. AND DECORTE, S. 1994. Termination of logic programs: the never-ending story. J. of
 Logic Programming 19–20, Supplement 1, 199–260. Special Issue: Ten Years of Logic Programming.
 GUPTA, G. ET AL. 2007. Coinductive logic programming and its applications. In ICLP'07. LNCS, vol.
 4670. 27–44. Interpreter Available at http://www.utdallas.edu/˜gupta/meta.html.
 GUPTA, G. AND COSTA, V.1994. Optimalimplementation of and-or parallel prolog. In PARLE'92.71–92.
 KOMENDANTSKAYA, E. ET AL. 2014a. Coalgebraic logic programming: from semantics to implementa
tion. J. Logic and Computation.
 KOMENDANTSKAYA, E. ET AL. 2014b. CoALP webpage: software and supporting documentation.
 http://staff.computing.dundee.ac.uk/katya/CoALP/.
 KOMENDANTSKAYA, E. ET AL. 2014c. Exploiting parallelism in coalgebraic logic programming.
 ENTCS 303, 121–148.
 KOMENDANTSKAYA,E. AND POWER, J. 2011. Coalgebraic derivations inlogic programming. In CSL'11.
 LIPIcs. Schloss Dagstuhl, 352–366.
 LLOYD, J. 1987. Foundations of Logic Programming, 2nd ed. Springer-Verlag.
 SIMON, L. ET AL. 2007. Co-logic programming: Extending logic programming with coinduction. In
 ICALP'07. LNCS, vol. 4596. 472–483.






































 AUNIFIEDFRAMEWORKFORGENERALIZED
 MULTICATEGORIES
 G.S.H.CRUTTWELLANDMICHAELA.SHULMAN
 Abstract. Notionsofgeneralizedmulticategoryhavebeendefinedinnumerouscon
textsthroughouttheliterature,andincludesuchdiverseexamplesassymmetricmulti
categories, globularoperads, Lawveretheories, andtopological spaces. Ineachcase,
 generalizedmulticategoriesaredefinedasthe“laxalgebras”or“Kleislimonoids”rela
tivetoa“monad”onabicategory. However, themeaningsof thesewordsdiffer from
 authortoauthor,asdothespecificbicategoriesconsidered.Weproposeaunifiedframe
work:byworkingwithmonadsondoublecategoriesandrelatedstructures(ratherthan
 bicategories),onecandefinegeneralizedmulticategoriesinawaythatunifiesallprevious
 examples,whileatthesametimesimplifyingandclarifyingmuchofthetheory.
 Contents
 1 Introduction 1
 2 Virtualdoublecategories 9
 3 Monadsonavirtualdoublecategory 14
 4 Generalizedmulticategories 20
 5 Compositesandunits 27
 6 2-categoriesofT-monoids 33
 7 Virtualequipments 36
 8 Normalization 43
 9 Representability 49
 A Composites inModandH-Kl 57
 B Comparisonstoprevioustheories 61
 1. Introduction
 Amulticategory isageneralizationof acategory, inwhichthedomainof amorphism,
 ratherthanbeingasingleobject, canbeafinitelistofobjects.Aprototypicalexample
 isthemulticategoryVectofvectorspaces, inwhichamorphism(V1,...,Vn) Wisa
 multilinearmap. Infact,anymonoidalcategorygivesamulticategoryinacanonicalway,
 wherethemorphisms(V1,...,Vn) WaretheordinarymorphismsV1⊗...⊗Vn W.
 ThefirstauthorwassupportedbyaPIMSCalgarypostdoctoral fellowship,andthesecondauthor
 byaNationalScienceFoundationpostdoctoral fellowshipduringthewritingofthispaper.
 2000MathematicsSubjectClassification: 18D05,18D20,18D50.
 Keywordsandphrases:Enrichedcategories,changeofbase,monoidalcategories,doublecategories,
 multicategories,operads,monads.
 cG.S.H.CruttwellandMichaelA.Shulman,2010.Permissiontocopyforprivateusegranted.
 1
2
 The multicategory Vect can be seen as arising in this way, but it is also natural to view
 its multicategory structure as more basic, with the tensor product then characterized as
 a representing object for “multimorphisms.” This is also the case for many other multi
categories; in fact, monoidal categories can be identified with multicategories satisfying a
 certain representability property (see [Her00] and §9).
 In addition to providing an abstract formalization of the passage from “multilinear
 map” to “tensor product,” multicategories provide a convenient way to present certain
 types of finitary algebraic theories (specifically, strongly regular finitary theories, whose
 axioms involve no duplication, omission, or permutation of variables). Namely, the objects
 of the multicategories are the sorts of the theory, and each morphism (X1,...,Xn)
 Y
 represents an algebraic operation of the theory. When viewed in this light, multicategories
 (especially those with one object, which correspond to one-sorted theories) are often
 called non-symmetric operads (see [May72]). The original definition of multicategories in
 [Lam69] (see also [Lam89]) was also along these lines (a framework for sequent calculus).
 The two viewpoints are related by the observation that when A is a small multicategory
 representing an algebraic theory, and C is a large multicategory such as Vect, a model
 of the theory A in C is simply a functor of multicategories A
 C. This is a version of
 the functorial semantics of [Law63].
 Our concern in this paper is with generalized multicategories, a well-known idea which
 generalizes the basic notion in two ways. Firstly, one allows a change of “base context,”
 thereby including both internal multicategories and enriched multicategories. Secondly,
 and more interestingly, one allows the finite lists of objects serving as the domains of
 morphisms to be replaced by “something else.” From the first point of view, this is
 desirable since there are many other contexts in which one would like to analyze the
 relationship between structures with coherence axioms (such as monoidal categories) and
 structures with universal or “representability” properties. From the second point of view,
 it is desirable since not all algebraic theories are strongly regular.
 For example, generalized multicategories include symmetric multicategories, in which
 the finite lists can be arbitrarily permuted. “Representable” symmetric multicategories
 correspond to symmetric monoidal categories. Enriched symmetric multicategories with
 one object can be identified with the operads of [May72, Kel05, KM95]. These describe
 algebraic theories in whose axioms variables can be permuted (but not duplicated or
 omitted). In most applications of operads (see [EM06, BM03] for some recent ones), both
 symmetry and enrichment are essential.
 An obvious variation of symmetric multicategories is braided multicategories. If we
 allow duplication and omission in addition to permutation of inputs, we obtain (multi
sorted) Lawvere theories [Law63]; a slight modification also produces the clubs of [Kel72b,
 Kel92]. There are also important generalizations to “algebraic theories” on more compli
cated objects; for instance, the globular operads of [Bat98, Lei04] describe a certain sort
 of algebraic theory on globular sets that includes many notions of weak n-category.
 A very different route to generalized multicategories begins with the observation
 of [Bar70] that topological spaces can be viewed as a type of generalized multicategory,
3
 when finite lists of objects are replaced by ultrafilters, and morphisms are replaced by a
 convergence relation. Many other sorts of topological structures, such as metric spaces,
 closure spaces, uniform spaces, and approach spaces, can also be seen as generalized
 multicategories; see [Law02, CT03, CHT04].
 With so many different faces, it is not surprising that generalized multicategories have
 been independently considered by many authors. They were first studied in generality by
 [Bur71], but have also been considered by many other authors, including [Lei04], [Lei02],
 [Her01], [CT03], [CHT04], [Bar70], [Web05], [BD98], [Che04], and [DS03]. While all these
 authors are clearly doing “the same thing” from an intuitive standpoint, they work in
 different frameworks at different levels of generality, making the formal definitions difficult
 to compare. Moreover, all of these approaches share a certain ad hoc quality, which, given
 the naturalness and importance of the notion, ought to be avoidable.
 In each case, the authors observe that the “something else” serving as the domain
 of morphisms in a generalized multicategory should be specified by some sort of monad,
 invariably denoted T. For example, ordinary multicategories appear when T is the “free
 monoid” monad, globular operads appear when T is the “free strict ω-category” monad,
 and topological spaces appear when T is the ultrafilter monad. All the difficulties then
 center around what sort of thing T is a monad on.
 Leinster [Lei02, Lei04] takes it to be a cartesian monad on an ordinary category C, i.e.
 Chas pullbacks, T preserves them, and the naturality squares for its unit and multiplica
tion are pullback squares. Burroni [Bur71], whose approach is basically the same, is able
 to deal with any monad on a category with pullbacks. Hermida [Her01] works with a carte
sian 2-monad on a suitable 2-category. Barr and Clementino et. al. [Bar70, CT03, CHT04]
 work with a monad on Set equipped with a “lax extension” to the bicategory of matri
ces in some monoidal category. Weber [Web05] works with a “monoidal pseudo alge
bra” for a 2-monad on a suitable 2-category. Baez-Dolan [BD98] and Cheng [Che04] (see
 also [FGHW08]) use a monad on Cat extended to the bicategory of profunctors (although
 they consider only the “free symmetric strict monoidal category” monad).
 Inspecting these various definitions and looking for commonalities, we observe that in
 all cases, the monads involved naturally live on a bicategory, be it a bicategory of spans
 (Burroni, Leinster), two-sided fibrations (Hermida), relations (Barr), matrices (Clementino
 et. al., Weber), or profunctors (Baez-Dolan, Cheng). What causes problems is that the
 monads of interest are frequently lax (preserving composition only up to a noninvertible
 transformation), but there is no obvious general notion of lax monad on a bicategory,
 since there is no good 2-category (or even tricategory) of bicategories that contains lax
 or oplax functors.
 Furthermore, merely knowing the bicategorical monad (however one chooses to formal
ize this) is insufficient for the theory, and in particular for the definition of functors and
 transformations between generalized multicategories. Leinster, Burroni, Weber, and Her
mida can avoid this problem because their bicategorical monads are induced by monads
 on some underlying category or 2-category. Others resolve it by working with an extension
 of a given monad on Set or Cat to the bicategory of matrices or profunctors, rather than
4
 merely the bicategorical monad itself. However, the various definitions of such extensions
 are tricky to compare and have an ad hoc flavor.
 Our goal in this paper (and its sequels) is to give a common framework which in
cludes all previous approaches to generalized multicategories, and therefore provides a
 natural context in which to compare them. To do this, instead of considering monads
 on bicategories, we instead consider monads on types of double categories. This essen
tially solves both problems mentioned above: on the one hand there is a perfectly good
 2-category of double categories and lax functors (allowing us to define monads on a double
 category), and on the other hand the vertical arrows of the double categories (such as
 morphisms in the cartesian category C, functions in Set, or functors between categories)
 provide the missing data with which to define functors and transformations of generalized
 multicategories.
 The types of double categories we use are neither strict or pseudo double categories,
 but instead an even weaker notion, for the following reason. An important intermediate
 step in the definition of generalized multicategories is the horizontal Kleisli construction
 of a monad T, whose (horizontal) arrows X
 Y are arrows X
 TY. Without strong
 assumptions on T, such arrows cannot be composed associatively, and hence the horizontal
 Kleisli construction does not give a pseudo double category or bicategory. It does, however,
 give a weaker structure, which we call a virtual double category.
 Intuitively, virtual double categories generalize pseudo double categories in the same
 way that multicategories generalize monoidal categories. There is no longer a horizontal
 composition operation, but we have cells of shapes such as the following:
 X0
 X0
 X0
 f
 Y0
 Y0
 p1
 X1
 X1
 p2
 X2
 X2
 α
 q
 p3
 · · ·
 · · ·
 pn
 Xn
 Xn
 Xn
 g
 Y1
 Y1
 We will give an explicit definition in §2. Virtual double categories have been studied
 by [Bur71] under the name of multicat´egories and by [Lei04] under the name of fc
multicategories, both of whom additionally described a special case of the horizontal
 Kleisli construction. They are, in fact, the generalized multicategories relative to the “free
 category” or “free double category” monad (depending on whether one works with spans
 or profunctors). In [DPP06] virtual double categories were called lax double categories,
 but we believe that name belongs properly to lax algebras for the 2-monad whose strict
 algebras are double categories. (We will see in Example 9.7 that oplax double categories
 in this “2-monadically correct” sense can be identified with a restricted class of virtual
 double categories.)
 Next, in §§3–4 we will show that for any monad T on a virtual double category X,
 one can define a notion which we call a T-monoid. In fact, we will construct an entire
 new virtual double category KMod(X,T) whose objects are T-monoids, by composing
 the “horizontal Kleisli” construction mentioned above with the “monoids and bimodules”
 construction Mod described in [Lei04, §5.3], which can be applied to any virtual double
5
 category. Then in §6 we will construct from KMod(X,T) a 2-category KMon(X,T) of T
monoids, T-monoid functors, and transformations, generalizing the analogous definition
 in [Lei04, §5.3]. This requires a notion of when a virtual double category has units, which
 we define in §5 along with the parallel notion of when it has composites. (These definitions
 generalize those of [Her00] and can also be found in [DPP06]; they are also a particular
 case of the “representability” of [Her01] and our §9.)
 For particular X and T, the notion of T-monoid specializes to several previous defini
tions of generalized multicategories. For example, if X consists of objects and spans in a
 cartesian category C and T is induced from a monad on C, we recover the definitions of
 Leinster, Kelly, and Burroni. And if X consists of sets and matrices enriched over some
 monoidal category V and T is a “canonical extension” of a taut set-monad to X, then we
 recover the definitions of Clementino et. al.
 However, the other definitions of generalized multicategory cannot quite be identified
 with T-monoids for any T, but rather with only a restricted class of them. For instance,
 if X consists of categories and profunctors, and T extends the “free symmetric monoidal
 category” monad on Cat (this is the situation of Baez-Dolan and Cheng), then T-monoids
 are not quite the same as ordinary symmetric multicategories. Rather, a T-monoid for
 this T consists of a category A, a symmetric multicategory M, and a bijective-on-objects
 functor from A to the underlying ordinary category of M. There are two ways to restrict
 the class of such T-monoids to obtain a notion equivalent to ordinary symmetric multi
categories: we can require A to be a discrete category (so that it is simply the set of
 objects of M), or we can require the functor to also be fully faithful (so that A is simply
 the underlying ordinary category of M). We call the first type of T-monoid object-discrete
 and the second type normalized.
 In order to achieve a full unification, therefore, we must give general definitions of
 these classes of T-monoid and account for their relationship. It turns out that this requires
 additional structure on our virtual double categories: we need to assume that horizontal
 arrows can be “restricted” along vertical ones, in a sense made precise in §7. Pseudo
 double categories with this property were called framed bicategories in [Shu08], where
 they were also shown to be equivalent to the proarrow equipments of [Woo82] (see also
 [Ver92]). Accordingly, if a virtual double category X has this property, as well as all units,
 we call it a virtual equipment.
 Our first result in §8, then, is that if T is a well-behaved monad on a virtual equip
ment, object-discrete and normalized T-monoids are equivalent. However, normalized
 T-monoids are defined more generally than object-discrete ones, and moreover when T
 which are insufficiently well-behaved, it is the normalized T-monoids which are of more
 interest. Thus, we subsequently discard the notion of object-discreteness. (Hermida’s gen
eralized multicategories also arise as normalized T-monoids, where X consists of discrete
 f
 ibrations in a suitable 2-category K and T is an extension of a suitable 2-monad on K.
 Weber’s definition is a special case, since as given it really only makes sense for generalized
 operads, for which normalization is automatic; see §B.16.) In Table 1 we summarize the
 meanings of T-monoids and normalized T-monoids for a number of monads T.
6
 MonadT on T-monoid Normalized
 T-Monoid
 Pseudo
 T-algebra
 Id V-Mat V-enriched
 category
 Set Set
 Id Span(C) Internal category
 inC
 ObjectofC ObjectofC
 Id Rel OrderedSet Set Set
 Id R+-Mat MetricSpace Set Set
 Powerset Rel ClosureSpace T1ClosureSpace Complete
 Semilattice
 Mod(powerset) 2-Prof Modular Closure
 Space
 ClosureSpace Meet-Complete
 Preorder
 Ultrafilter Rel TopologicalSpace T1space Compact
 Hausdorffspace
 Mod(ultrafilter) 2-Prof ModularTop.
 Space
 TopologicalSpace OrderedCompact
 Hausdorffspace
 Ultrafilter R+-Mat Approachspace ? Compact
 Hausdorffspace
 Freemonoid Span(Set) Multicategory ? Monoid
 Mod(freemonoid) Set-Prof “Enhanced”
 multicategory
 Multicategory Monoidal
 category
 Free sym. strict
 mon.cat.
 Set-Prof “Enhanced” sym.
 multicategory
 Symmetric
 multicategory
 Symmetric mon.
 cat.
 Freecategory Span(Grph) Virtualdouble
 category
 ? Category
 Mod(freecategory) Prof(Grph) ? Virtualdouble
 category
 Pseudo double
 category
 Freecat.w/
 finiteproducts
 Set-Prof ? Multi-sorted
 Lawveretheory
 Cat. w/ finite
 products
 Freecat.w/
 smallproducts
 Set-Profls ? MonadonSet Cat. w/ small
 products
 Freepresheaf
 Sop Set
 Span Setob(S) FunctorA S FunctorA S
 w/discretefibers
 Functor
 Sop Set
 Mod(freepresheaf) Prof(Setob(S)) ? FunctorA S Pseudofunctor
 Sop Cat
 Freestrict
 ω-category
 Span(Globset) Multi-sorted
 globularoperad
 ? Strictω-category
 Mod(freeω-cat.) Prof(Globset) ? Multi-sorted
 globularoperad
 Monoidal
 globularcat.
 FreeM-set (Ma
 monoid)
 Span(Set) M-graded
 category
 ? M-set
 Table1:Examplesofgeneralizedmulticategories.Theboxesmarked“?”donothaveany
 establishedname; inmostcasestheyalsodonotseemveryinteresting.
7
 Now, what determines whether the “right” notion of generalized multicategory is a
 plain T-monoid or a normalized one? The obvious thing distinguishing the situations of
 Leinster, Burroni, and Clementino et. al. from those of Baez-Dolan, Cheng, and Hermida
 is that in the former case, the objects of X are “set-like,” whereas in the latter, they are
 “category-like.” However, some types of generalized multicategory can be constructed
 starting from two different monads on two different virtual equipments, one of which
 belongs to the first group and the other to the second.
 For example, observe that an ordinary (non-symmetric) multicategory has an under
lying ordinary category, containing the same objects but only the morphisms (V1)
 W
 with unary source. Thus, such a multicategory can be defined in two ways: either as
 extra structure on its set of objects, or as extra structure on its underlying category. In
 the second case, normalization is the requirement that in the extra added structure, the
 multimorphisms with unary source do no more than reproduce the originally given cate
gory. Thus, ordinary multicategories arise both as T-monoids the “free monoid” monad
 on sets and spans, and as normalized T-monoids for the “free monoidal category” monad
 on categories and profunctors.
 Our second result in §8 is a generalization of this relationship. We observe that
 the virtual equipment of categories and profunctors results from applying the “monoids
 and modules” construction Mod to the virtual equipment of sets and spans. Thus, we
 generalize this situation by showing that for any monad T on a virtual equipment, plain
 T-monoids can be identified with normalized Mod(T)-monoids. That this is so in the
 examples can be seen by inspection of Table 1. Moreover, it is sensible because application
 of Mod takes “set-like” things to “category-like” things.
 It follows that the notion of “normalized T-monoid” is actually more general than
 the notion of T-monoid, since arbitrary T-monoids for some T can be identified with the
 normalized S-monoids for some S (namely S = Mod(T)), whereas normalized S-monoids
 cannot always be identified with the arbitrary T-monoids for any T. (For instance, this is
 not the case when S is the “free symmetric monoidal category” monad on categories
 and profunctors.) This motivates us to claim that the “right” notion of generalized
 multicategory is a normalized T-monoid, for some monad T on a virtual equipment.
 Having reached this conclusion, we also take the opportunity to propose a new naming
 system for generalized multicategories which we feel is more convenient and descriptive.
 Namely, if (pseudo) T-algebras are called widgets, then we propose to call normalized
 T-monoids virtual widgets. The term “virtual double category” is of course a special
 case of this: virtual double categories are the normalized T-monoids for the monad T on
 Prof(Grph) whose algebras are double categories.
 Of course, “virtual” used in this way is a “red herring” adjective1 akin to “pseudo” and
 “lax”, since a virtual widget is not a widget. The converse, however, is true: every widget
 has an underlying virtual widget, so the terminology makes some sense. For example, the
 observation above that every monoidal category has an underlying multicategory is an
 1The mathematical red herring principle states that an object called a “red herring” need not, in
 general, be either red or a herring.
8
 instance of this fact. Moreover, it often happens that virtual widgets share many of the
 same properties as widgets, and many theorems about widgets can easily be extended to
 virtual widgets. Thus, it is advantageous to use a terminology which stresses the close
 connection between the two. Another significant advantage of “virtual widget” over “T
multicategory” is that frequently one encounters monads T for which T-algebras have
 a common name, such as “double category” or “symmetric monoidal category,” but T
 itself has no name less cumbersome than “the free double category monad” or “the free
 symmetric monoidal category monad.” Thus, it makes more sense to name generalized
 multicategories after the algebras for the monad than after the monad itself.
 By the end of §8, therefore, we have unified all existing notions of generalized multi
category under the umbrella of virtual T-algebras, where T is a monad on some virtual
 equipment. Since getting to this point already takes us over 40 pages, we leave to future
 work most of the development of the theory and its applications, along with more specific
 comparisons between existing theories (see [CS10a, CS10b]).
 However, we do spend some time in §9 on the topic of representability. This is a central
 idea in the theory of generalized multicategories, which states that any pseudo T-algebra
 (or, in fact, any oplax T-algebra) has an underlying virtual T-algebra. Additionally, one
 can characterize the virtual T-algebras which arise in this way by a “representability”
 property. This can then be interpreted as an alternate definition of pseudo T-algebra
 which replaces “coherent algebraic structure” by a “universal property,” as advertised
 in [Her01]. In addition to the identification of monoidal categories with “representable”
 multicategories, this also includes the fact that compact Hausdorff spaces are T1 spaces
 with additional properties, and that fibrations over a category S are equivalent to pseudo
functors Sop
 Cat. In [CS10b] we will extend more of the theory of representability
 in [Her01] to our general context.
 Finally, the appendices are devoted to showing that all existing notions of generalized
 multicategory are included in our framework. In Appendix A we prepare the way by
 giving sufficient conditions for our constructions on virtual double categories to preserve
 composites, which is important since most existing approaches use bicategories. Then in
 Appendix B we summarize how each existing theory we are aware of fits into our context.
 We have chosen to postpone these comparisons to the end, so that the main body of
 the paper can present a unified picture of the subject, in a way which is suitable also as
 an introduction for a reader unfamiliar with any of the existing approaches. It should be
 noted, though, that we claim no originality for any of the examples or applications, or
 the ideas of representability in §9. Our goal is to show that all of these examples fall into
 the same framework, and that this general framework allows for a cleaner development of
 the theory.
 1.1. Acknowledgements. The first author would like to thank Bob Par´e for his sug
gestion to consider “double triples”, as well as helpful discussions with Maria Manuel
 Clementino, Dirk Hofmann, and Walter Tholen. The second author would like to thank
 David Carchedi and the patrons of the n-Category Caf´e blog for several helpful conversa
tions. Both authors would like to thank the editor and the referee for helpful suggestions.
9
 1. Virtual double categories
 The definition of virtual double category may be somewhat imposing, so we begin with
 some motivation that will hopefully make it seem inevitable. We seek a framework which
 includes all sorts of generalized multicategories. Since categories themselves are a particu
lar sort of generalized multicategory (relative to an identity monad), our framework should
 in particular include all sorts of generalized categories. In particular, it should include
 both categories enriched in a monoidal category V and categories internal to a category
 Cwith pullbacks, so let us begin by considering how to unify these two situations.
 We start by recalling that both V-enriched categories and C-internal categories are
 particular cases of monoids in a monoidal category. On the one hand, if V is a cocomplete
 closed monoidal category and O is a fixed set, then V-enriched categories with object
 set O can be identified with monoids in the monoidal category of O-graphs in V—i.e.
 (O × O)-indexed families of objects of V, with monoidal structure given by “matrix
 multiplication.” On the other hand, if C is a category with pullbacks and O is an object
 of C, then C-internal categories with object-of-objects O can be identified with monoids
 in the monoidal category of O-spans in C—i.e. diagrams of the form O ← A → O, with
 monoidal structure given by span composition.
 Now, both of these examples share the same defect: they require us to fix the objects
 (the set O or object O). In particular, the morphisms of monoids in these monoidal
 categories are functors which are the identity on objects. It is well-known that one can
 eliminate this fixing of objects by combining all the monoidal categories of graphs and
 spans, respectively, into a bicategory. (In essense, this observation dates all the way back
 to [B´en67].) In the first case the relevant bicategory V-Mat consists of V-matrices: its
 objects are sets, its arrows from X to Y are (X × Y)-matrices of objects in V, and its
 composition is by “matrix multiplication.” In the second case the relevant bicategory
 Span(C) consists of C-spans: its objects are objects of C, its arrows from X to Y are
 spans X ←A→Y in C, and its composition is by pullback. It is easy to define monoids
 in a bicategory to generalize monoids in a monoidal category2.
 However, we still have the problem of functors. There is no way to define morphisms
 between monoids in a bicategory so as to recapture the correct notions of enriched and
 internal functors in V-Mat and Span(C). But we can solve this problem if instead of
 bicategories we use (pseudo) double categories, which come with objects, two different
 kinds of arrow called “horizontal” and “vertical,” and 2-cells in the form of a square:
 2Monoids in a bicategory are usually called monads. However, we avoid that term for these sorts of
 monoids for two reasons. Firstly, the morphisms of monoids we are interested in are not the same as the
 usual morphisms of monads (although they are related; see [LS02, §2.3–2.4]). Secondly, there is potential
 for confusion with the monads on bicategories and related structures which play an essential role in the
 theory we present.
10
 BothV-Mat andSpan(V)naturallyenlargetopseudodoublecategories, interpreting
 theirexistingarrowsandcompositionashorizontalandaddingnewverticalarrows. For
 V-Mat thenewvertical arrowsare functionsbetweensets,while forSpan(C)thenew
 vertical arrowsaremorphisms inC. Wecannowdefinemonoids inadoublecategory
 (relativetothehorizontal structure)andmorphismsbetweensuchmonoids(makinguse
 oftheverticalarrows)soastorecapturethecorrectnotionof functor inbothcases(see
 Definition2.8).
 Thefinalgeneralizationfrompseudodoublecategoriestovirtualdoublecategoriesis
 moredifficult tomotivateat themoment,butasremarkedinthe introduction,wewill
 finditessential in§4.Conceptually(and, infact, formally),avirtualdoublecategoryis
 relatedtoapseudodoublecategoryinthesamewaythatamulticategoryisrelatedtoa
 monoidal category. Thus, justasonecandefinemonoids inanymulticategory, onecan
 likewisedosoinanyvirtualdoublecategory.
 2.1. Definition.AvirtualdoublecategoryXconsistsof thefollowingdata.
 •AcategoryX(theobjectsandverticalarrows),withthearrowswrittenvertically:
 X
 Y
 f
 •Forany twoobjectsX,Y ∈X, aclassof horizontal arrows,writtenhorizontally
 withaslashthroughthearrow:
 X Y p
 •Cells,withverticalsourceandtarget,andhorizontalmulti-sourceandtarget,written
 asfollows:
 Y0 Y1 q
 X0
 Y0
 f
 X0 Xn Xn
 Y1
 g
 X0 X1
 p1 X1 X2
 p2 X2 ··· p3 ··· Xn
 pn
 α (2.2)
 Note that this includescellswithsourceof length0, inwhichcasewemust have
 X0=Xn; suchcellsarevisuallyrepresentedas follows:
 X
 Y0
 f
 X
 Y1
 g
 4 4 4 4 4 4 4 4
 Y0 Y1 q
 α
11
 •Forthefollowingconfigurationofcells,
 Z0 Z1 r
 Y0
 Z0
 g0
 Y0 Ym Ym
 Z1
 g1
 Y0 Y1 q1
 X0
 Y0
 f0
 X0 Xn1
 p11...p1n1 _ _ _ _ _ _ _ Xn1
 Y1
 f1
 Y1 Y2 q2
 Xn1
 Y1
 Xn1
 Xn2
 p21...p2n1 _ _ _ _ _ _ _ Xn2
 Y2
 f2
 Xn2
 ··· ··· _ _ _ _ _ _ _ ··· Xnm
 ··· _ _ _ _ _ _ _
 Y2 Ym q3···qm
 _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
 Xnm
 Ym
 fm α1 α2 α3···αm
 β
 acompositecell
 Z0 Z1 r
 Y0
 Z0
 g0
 Y0 Ym Ym
 Z1
 g1
 Y0
 X0
 Y0
 f0
 X0 Xn1
 p11...p1n1 _ _ _ _ _ _ _ Xn1
 Xn1
 Xn1
 Xn2
 p21...p2n1 _ _ _ _ _ _ _ Xn2
 Xn2
 ··· ··· _ _ _ _ _ _ _ ··· Xnm
 ··· _ _ _ _ _ _ _ Xnm
 Ym
 fm
 β(αm⊡···⊡α1)
 •Foreachhorizontalarrowp,anidentitycell
 X Y p
 X Y p
 X
 X
 Y
 Y
 1p
 •Associativity and identity axioms for cell composition. The associativity axiom
 statesthat
 γ(βm⊡···⊡β1) (αmkm
 ⊡···⊡α11)=γ βm(αmkm
 ⊡···⊡αm1)⊡···⊡β1(α1k1
 ⊡···⊡α11)
 whiletheidentityaxiomsstatethat
 α(1p1
 ⊡···⊡1pn
 )=α and 1q(α1)=α1
 whenevertheseequationsmakesense.
 2.3. Remark.Asmentioned inthe introduction, virtual doublecategorieshavealso
 beencalledfc-multicategoriesbyLeinster[Lei04]andmulticat´egoriesbyBurroni [Bur71].
 Our terminologyischosentoemphasizetheircloserelationshipwithdoublecategories,
 andtofit intothegeneralnamingschemeof§9.
 2.4. Remark.Inmuchofthedouble-categoryliterature, itiscommonforthe“slashed”
 arrows(spans,profunctors,etc.) tobethevertical arrows.Wehavechosentheopposite
 conventionpurelyforeconomyof space: thecells inavirtualdoublecategoryfitmore
 convenientlyonapagewhentheirmulti-sourceisdrawnhorizontally.
12
 2.5. Examples.Assuggested bythediscussion at the beginning of this section, monoidal
 categories, bicategories, 2-categories, multicategories, and pseudo double categories can
 each be regarded as examples of virtual double categories, by trivializing the vertical or
 horizontal structure in various ways; see [Lei02, p. 4] or [Lei04, §5.1] for details.
 We now present the two virtual double categories that will serve as initial inputs for
 most our examples: spans and matrices. (Both are also described in [Lei04, Ch. 5].) For
 consistency, we name all of our virtual double categories by their horizontal arrows, rather
 than their vertical arrows or objects.
 2.6. Example. Let (V,⊗,I) be a monoidal category. The virtual double category
 V-Mat is defined as follows: its objects are sets, its vertical arrows are functions, its
 horizontal arrows X p Y are families {p(y,x)}x∈X,y∈Y of objects of V (i.e. (X × Y )
matrices), and a cell of the form (2.2) consists of a family of V-arrows
 p1(x1, x0) ⊗ p2(x2,x1) ⊗ ··· ⊗ pn(xn,xn−1) α q(fxn,gx0),
 one for each tuple (x0,...,xn) ∈ X0 ×···×Xn. When n = 0, of course, the n-ary tensor
 product on the left is to be interpreted as the unit object of V.
 In particular, if V is the 2-element chain 0 ≤ 1, with ⊗ given by ∧, then the horizontal
 arrows of V-Mat are relations. In this case we denote V-Mat by Rel.
 It is well-known that V-matrices form a bicategory (and, in fact, a pseudo double
 category) as long as V has coproducts preserved by ⊗. However, if we merely want a
 virtual double category, we see that this requirement is unnecessary. (In fact, V could be
 merely a multicategory itself.)
 2.7. Example. For a category C with pullbacks, the virtual double category Span(C)
 is defined as follows: its objects and vertical arrows are those of C, its horizontal arrows
 X p Y arespans X P Y,andacellofthe form (2.2) is a morphism of spans
 P1 ×X1 
P2 ×X2 
···×Xn−1 
Pn 
α Q
 lying over f and g. When n = 0, the n-ary span composite in the domain is to be
 interpreted as the identity span X0
 X0
 X0.
 Note that in this case, we do need to require that C have pullbacks. If C does not
 have pullbacks, a more natural setting would be to consider Span(C) as a “co-virtual
 double category”, in which the horizontal target of a cell is a string of horizontal arrows.
 However, co-virtual double categories do not provide the structure necessary to define
 generalized multicategories.
 We now recall the construction of monoids and modules in a virtual double category
 from [Lei04, §5.3].
13
 2.8. Definition.LetXbeavirtualdoublecategory.ThevirtualdoublecategoryMod(X)
 hasthefollowingcomponents:
 •Theobjects (monoids) consist of fourparts (X0,X,¯ x,ˆ x): anobjectX0 ofX, a
 horizontalendo-arrowX0
 X X0 inX,andmultiplicationandunitcells
 X0 X0
 X X0 X0
 X X0
 X0
 X0
 X0 X0 X0 X
 ¯ x and
 X0
 X0
 X0
 X0
 4 4 4 4 4 4 4
 4 4 4 4 4 4 4
 X0 X0 X
 ˆ x
 satisfyingassociativityandidentityaxioms.
 •Thevertical arrows (monoidhomomorphisms)consist of twoparts (f0,f): a
 verticalarrowX0
 f0 Y0 inXandacell inX:
 X0 X0
 X
 Y0 Y0 Y
 X0
 Y0
 f0
 X0
 Y0
 f0 f
 whichiscompatiblewiththemultiplicationandunitsofXandY.
 •Thehorizontalarrows(modules)consistofthreeparts(p,¯ pr,¯ pl):ahorizontalarrow
 X0
 p Y0 inXandtwocellsinX:
 X0 X0
 X X0 Y0
 p X0
 X0
 Y0
 Y0 X0 Y0 p
 ¯ pr and
 X0 Y0
 p Y0 Y0
 Y X0
 X0
 Y0
 Y0 X0 Y0 p
 ¯ pl
 whicharecompatiblewiththemultiplicationandunitsofXandY.
 •ThecellsarecellsinX:
 (Y0)0 (Y1)0
 (X0)0
 (Y0)0
 f0
 (X0)0 (Xn)0 (Xn)0
 (Y1)0
 g0
 (Y0)0 (Y1)0 q
 (X0)0 (X1)0
 p1 (X1)0 (X2)0
 p2 (X2)0 ··· p3 ··· (Xn)0
 pn
 α
 whicharecompatiblewiththe leftandrightactionsof thehorizontalcells.
 Notethat,asobservedin[Lei04, §5.3],wecandefineMod(X)withoutrequiringany
 hypothesesonthevirtualdoublecategoryX, incontrasttothesituationforbicategories
 orpseudodoublecategories.
14
 2.9. Example. We denote the virtual double category Mod(V-Mat) by V-Prof; its
 objects are V-enriched categories, its vertical arrows are V-functors, its horizontal arrows
 are V-profunctors, and its cells are a generalization of the “forms” of [DS97] (including,
 as a special case, natural transformations between profunctors). When V is closed (hence
 enriched over itself) and symmetric, V-profunctors C H D can be identified with V
functors Dop × C
 V.
 Again, note that because we are working with virtual double categories, we do not
 require that V have any colimits (in fact, V could be merely a multicategory).
 2.10. Example.Let C be a category with pullbacks. We denote the virtual double cat
egory Mod(Span(C)) by Prof(C); it consists of internal categories, functors, profunctors,
 and transformations in C.
 Note that Set-Mat ∼ = Span(Set) and thus Set-Prof ∼
 =Prof(Set).
 1. Monads on a virtual double category
 We claimed in §1 that the “inputs” of a generalized multicategory are parametrized by
 a monad. Why should this be so? Suppose that we have an operation T which, given a
 set (or object) of objects X, produces a set (or object) TX intended to parametrize such
 inputs. For “ordinary” multicategories, TX will be the set of finite lists of elements of X.
 Now, from the perspective of the previous section, the data of a category includes
 an object A0 and a horizontal arrow A0
 A A0 in some virtual double category. For
 example, if we work in Set-Mat, then A is a matrix consisting of the hom-sets A(x,y)
 for every x,y ∈ A0. Now, instead, we want to have hom-sets A(x,y) whose domain x is
 an element of TA0. Thus, it makes sense to consider a horizontal arrow A0
 A TA0 as
 part of the data of a T-multicategory. (We use A0
 TA0 rather than TA0
 A0, for
 consistency with Examples 2.9 and 2.10: the codomain of the horizontal arrow datum of
 a monoid specifies the domains of the arrows in that monoid.)
 However, we now need to specify the units and composition of our generalized multi
category. The unit should be a cell into A with 0-length domain, but its source and
 target vertical arrows can no longer both be identities because A0= TA0. In an ordinary
 multicategory, the identities are morphisms (x) 1x x whose domain is a singleton list;
 in terms of Set-Mat this can be described by a cell
 •••••••
 A0
 A0
 •
 A0
 A0 
••••••••
 A
 ?
 ?
 ?
 ?
 ?
 η
 ?
 ?
 ?
 TA0
 TA0
 where A0 
η TA0 is the inclusion of singleton lists.
15
 Regarding composition, in an ordinary multicategory we can compose a morphism
 (y1, . . ., yn) g z not with a single morphism, but with a list of morphisms (f1,...,fn)
 where (xi1,...,xiki
 ) fi yi. In terms of Set-Mat this represents the fact that we cannot
 ask for a multiplication cell with domain A
 A , since the domain of A does not
 match its codomain, but instead we can consider a cell with domain A
 TA ,where we
 extend T to act on Set-matrices in the obvious way. Now, however, the codomain of TA
 is T2A0; in order to have a cell with codomain A we need to “remove parentheses” from
 the resulting domain ((x11,...,x1k1
 ),...,(xn1,...,xnkn
 )) to obtain a single list. Thus the
 composition should be a cell
 A0
 A0
 A0
 A0
 A0
 TA0
 TA
 A TA0 T2A0
 T2A0
 T2A0
 µ
 A
 TA0
 TA0
 where µ is the “remove parentheses” function. Of course, these functions η and µ are the
 structure maps of the “free monoid” monad on Set. Thus we see that in order to define
 ordinary multicategories, what we require is an “extension” of this monad to Set-Mat.
 In order to have a good notion of a monad on a virtual double category, we need at
 least a 2-category of virtual double categories. Since virtual double categories are them
selves a special case of generalized multicategories, it suffices to observe that generalized
 multicategories of any sort form a 2-category. However, since we have not yet defined
 generalized multicategories in our context, at this point in our exposition it is appropriate
 to give an explicit description of the 2-category vDbl.
 Of course, the objects of vDbl are virtual double categories, and its 1-morphisms
 (called functors of virtual double categories) are the obvious structure-preserving maps:
 functions from the objects, vertical and horizontal arrows, and cells of the domain to
 those of the codomain, preserving all types of source, target, identities, and composition.
 However, the definition of 2-morphisms in vDbl is slightly less obvious.
 3.1. Definition. Given functors X F
 G
 Yofvirtual double categories, a transforma
tion F θ Gconsists of the following data.
 • For each object X in X, a vertical arrow FX θX GX, which form the components
 of a natural transformation between the vertical parts of F and G.
 • For each horizontal arrow X p Y in X, a cell in Y:
 FX
 FX
 θX
 GX
 GX
 Fp
 θp
 Gp
 FY
 FY
 θY
 GY
 GY
 (3.2)
16
 • An axiom asserting that θ is “cell-natural,” meaning that
 θq(Fα) = (Gα)(θp1 
⊡ ···⊡θpn
 )
 whenever this makes sense.
 Virtual double categories, functors, and transformations form a 2-category denoted vDbl.
 3.3. Example.AnylaxmonoidalfunctorV NWinducesfunctorsV-Mat N∗ W-Mat
 and V-Prof N∗ W-Prof in an evident way. Moreover, any monoidal natural transfor
mation N ψ M between lax monoidal functors induces transformations N∗ 
ψ∗ M∗ in
 both cases. In this way (−)-Mat and (−)-Prof become 2-functors from the 2-category of
 monoidal categories to vDbl.
 3.4. Example.Similarly, any pullback-preserving functor C N D between categories
 with pullbacks induces functors Span(C) N∗ Span(D) and Prof(C) N∗ Prof(D), and
 any natural transformation N ψ M between such functors induces transformations
 N∗ 
ψ∗ M∗, thereby making Span(−) and Prof(−) into 2-functors as well.
 3.5. Example. When restricted to bicategories or pseudo double categories, functors
 of virtual double categories are equivalent to the usual notions of lax functor.
 This is a special case of a general fact; see Theorem 9.13. When transformations of
 virtual double categories are similarly restricted, they become icons in the sense of [Lac10]
 (for bicategories) and vertical transformations (for pseudo double categories).
 By a monad on a virtual double category X, we will mean a monad in the 2-category
 vDbl. Thus, it consists of a functor T : X
 X and transformations η: Id
 µ: TT
 T and
 T satisfying the usual axioms. We now give the examples of such monads that
 we will be interested in.
 3.6. Example. Since 2-functors preserve monads, any pullback-preserving monad on a
 category C with pullbacks induces monads on Span(C) and Prof(C). Examples of such
 monads include the following.
 • The “free monoid” monad on Set (or, more generally, on any countably lextensive
 category).
 • The “free M-set” monad (M ×−) on Set, for any monoid M (or more generally,
 for any monoid object in a category with finite limits).
 • The monad (−)+1 on any lextensive category.
 • The “free category” monad on the category of directed graphs.
 • The “free strict ω-category” monad on the category of globular sets.
17
 Many more examples can be found in [Lei04, pp. 103–107]; see also §B.1. By the argument
 above, each of these monads extends to a monad on a virtual double category of spans.
 The assignments V → V-Mat and V → V-Prof are also 2-functorial, but the monads
 we obtain in this way from monads on monoidal categories are not usually interesting for
 defining multicategories. However, there are some general ways to construct monads on
 virtual double categories of matrices, at least when V is a preorder. The following is due
 to [Sea05], which in turn expands on [CHT04].
 3.7. Example. By a quantale we mean a closed symmetric monoidal complete lattice.
 A quantale is completely distributive if for any b ∈ V we have b = {a | a ≺ b},
 where a ≺ b means that whenever b ≤ S then there is an s ∈ S with a ≤ s. (If in this
 definition S is required to be directed, we obtain the weaker notion of a continuous lattice.)
 For us, the two most important completely distributive quantales are the following.
 • The two-element chain 2 = (0 ≤ 1).
 • The extended nonnegative reals R+ = [0,∞] with the reverse of the usual ordering
 and ⊗ =+.
 A functor said to be taut if it preserves pullbacks of monomorphisms (and therefore
 also preserves monomorphisms). A monad is taut if its functor part is taut, and moreover
 the naturality squares of η and µ for any monomorphism are pullbacks. Some important
 taut monads on Set are the identity monad, the powerset monad (whose algebras are
 complete lattices), the filter monad, and the ultrafilter monad (whose algebras are compact
 Hausdorff spaces).
 Now let V be a completely distributive quantale and T a taut monad on Set. For a
 V-matrix X p Y and elements F ∈ TX and G ∈TY, define
 Tp(G,F) =
 v ∈V ∀B⊆Y : G∈TB⇒F∈T(pv[B]) ,
 where
 pv[B] = x ∈X ∃y∈B:v≤p(y,x) .
 It is proven in [Sea05] that this action on horizontal arrows extends T to a monad on
 V-Mat. (Actually, Seal shows that it is a “lax extension of T to V-Mat with op-lax unit
 and counit”; we will show in §B.6 that this is the same as a monad on V-Mat.)
 In [Sea05] this monad on V-Mat is called the “canonical extension” of T (note, how
ever, that it is written backwards from his definition, as our Kleisli arrows will be X
 whereas his are TX
 TY,
 Y). Since V-Mat is isomorphic to its “horizontal opposite,” there
 is also an “op-canonical extension”, which is in general distinct (although in some cases,
 such as for the ultrafilter monad, the two are identical). There are also many other
 extensions: for more detail, see [SS08].
 Another general way of constructing monads on virtual double categories is to apply
 the construction Mod from the previous section, which turns out to be a 2-functor. Its 1
functoriality is fairly obvious and was described in [Lei04, §5.3]; its action on 2-morphisms
 is given as follows.
18
 3.8. Definition.Let X F
 G
 Ybefunctors between virtual double categories, and F θ G
 a transformation. One can define a transformation
 Mod(F) Mod(θ) Mod(G)
 whose vertical-arrow component at an object (X0,X, ¯ x, ˆ x) is the monoid homomorphism
 FX0
 FX0
 θX0
 GX0
 GX0
 F(X)
 θX
 G(X)
 FX0
 FX0
 θX0
 GX0
 GX0
 and whose cell component at a horizontal arrow (p, ¯ pr, ¯ pl) is given by
 FX0
 FX0
 θX0
 GX0
 GX0
 Fp
 θp
 Gp
 FY0
 FY0
 θY0
 GY0
 GY0
 3.9. Proposition. With action on objects, 1-cells, and 2-cells described above, Mod is
 an endo-2-functor of vDbl.
 Note that the 2-functors (−)-Prof and Prof(−) can now be seen as the composites of
 Mod with (−)-Mat and Span(−), respectively.
 3.10. Corollary.A monad T on a virtual double category X induces a monad Mod(T)
 on Mod(X).
 3.11. Example. Any monad T on V-Mat induces a monad on V-Prof. For instance,
 this applies to the monads constructed in Example 3.7.
 3.12. Example. Let V be a symmetric monoidal category with an initial object ∅
 preserved by ⊗. Then the “free monoid” monad T on Set extends to a monad on V-Mat
 as follows: a V-matrix X p Y is sent to the matrix TX Tp TY defined by
 Tp (y1,...,ym),(x1,...,xn) = p(y1,x1) ⊗ ... ⊗p(yn,xn) if n = m
 ∅
 if n= m
 Applying Mod, we obtain an extension of the “free strict monoidal V-category” monad
 from V-Cat to V-Prof.
19
 3.13. Example. Likewise, any monad T on Span(C) extends to a monad on Prof(C).
 But most interesting monads on Span(C) are induced from C, so this gains us little
 beyond the observation that Prof(−) is a 2-functor.
 Not every monad on V-Prof or Prof(C) is induced by one on V-Mat or Span(C),
 however. The following examples are also important.
 3.14. Example.Let V beasymmetric monoidal category with finite colimits preserved
 by ⊗ on both sides. Then there is a “free symmetric strict monoidal V-category” monad
 T on V-Cat, defined by letting the objects of TX be finite lists of objects of X, with
 
 
 TX (x1,...,xn),(y1,...,ym) =
 σ∈Sn1≤i≤n
 ∅
 X(xσ(i), yi) if n = m
 if n= m.
 Anearly identical-looking definition for profunctors extends this T to a monad on V-Prof.
 A similar definition applies for braided monoidal V-categories.
 3.15. Example.For V asin Example 3.14, there is also a “free V-category with strictly
 associative finite products” monad on V-Cat. The objects of this TX are again finite lists
 of objects of X, but now we have
 TX (x1,...,xm),(y1,...,yn) =
 X(xj,yi).
 1≤i≤n1≤j≤m
 If V is cartesian monoidal, then this can equivalently be written as
 TX (x1,...,xm),(y1,...,yn) =
 X(xα(i), yi).
 α: n→m1≤i≤n
 Again, a nearly identical definition for profunctors extends this to a monad on V-Prof.
 3.16. Example.Monadsthatfreely adjoin other types of limits and colimits also extend
 from V-Cat to V-Prof in a similar way. For instance, if V is a locally finitely presentable
 closed monoidal category as in [Kel82], there is a “free V-category with cotensors by
 f
 initely presentable objects” monad on V-Cat. An object of TX consists of a pair3 (v;x)
 where x ∈ X and v ∈V is finitely presentable. On homs we have
 TX(v;x),(w;y) = w,X(x,y)⊗v .
 As before, a nearly identical definition extends this to V-Prof.
 3To be precise, this definition only gives a pseudomonad on V-Cat. It is, however, easy to modify it
 to make a strict monad.
20
 1. Generalizedmulticategories
 Wenowlackonlyonefinal ingredient for thedefinitionof generalizedmulticategories.
 Sincemulticategories are like categories, we expect themtoalsobemonoids insome
 virtual doublecategory. However, aswehave seen in§3, theirunderlyingdatashould
 includeahorizontalarrowA0 TA0ratherthanA0 A0.Thusweneedtoconstruct,
 givenTandX, avirtualdoublecategoryinwhichthehorizontal arrowsarehorizontal
 arrowsoftheformA0 TA0 inX.Thisisthepurposeofthefollowingdefinition.
 4.1. Definition.LetTbeamonadonavirtual doublecategoryX. Definethehori
zontalKleislivirtualdoublecategoryofT,H-Kl(X,T),as follows.
 • ItsverticalcategoryisthesameasthatofX.
 •AhorizontalarrowX p Y isahorizontalarrowX p TY inX.
 •Acellwithnullarysourceusestheunitof themonad,sothatacell
 X
 Y
 f
 X
 Z
 g
 4 4 4 4 4 4 4 4
 Y Z p
 α
 inH-Kl(X,T) isacell
 X
 Y
 f
 X
 TX
 η , , , , ,
 TX
 TZ
 Tg , , , , ,
 Y TZ p
 α
 inX(notethatTg◦η=η◦gbynaturality).
 •Acellwithnon-nullarysourceusesthemultiplicationof themonad,sothatacell
 Y0 Y1
 X0
 Y0
 f
 X0 Xn Xn
 Y1
 g
 Y0 Y1 q
 X0 X1
 p1 X1 X2
 p2 X2 ··· p3 ··· Xn
 pn
 α
21
 inH-Kl(X,T) isacell
 X0
 Y0
 f
 Y0 TY1 q
 X0 TX1
 p1 TX1 T2X2
 Tp2 T2X2 ··· T2p3 ··· TnXn
 Tn−1pnTnXn
 . . .
 µ
 . . .
 TXn
 µ
 TXn
 TY1
 Tg
 α
 inX(notethatTg◦µn−1=µn−1◦Tng,bynaturality).
 •Thecompositeof
 ···
 α1
 ···
 α2
 ···
 αn ···
 β
 isgivenbythecompositeof
 α1
 ···
 µ
 ···
 µ
 µ
 µ
 ···
 ···
 ···
 µ
 µ
 Tµ
 Tα2
 ···
 Tµ
 µ
 µ µ
 µ
 Tµ
 T2µ
 T2α3
 ··· ···
 ··· ···
 ···
 µ
 µ
 Tµ
 T2µ
 T3α4
 µ µ
 µ µ
 Tµ Tµ
 ··· ···
 ···
 ···
 ··· ···
 ···
 ···
 ···
 Tn−2µ Tn−2µ ···
 Tn−1αn
 β
 inX.
 • IdentitycellsusethoseofX:
 X TY p
 X TY p
 X
 X
 TY
 TY
 1P
22
 In general, the associativity for H-Kl(X,T) is shown by using the (cell) naturality of
 µ and η, as well as the monad axioms. The general associativity is too large a diagram
 to show here; instead, we will demonstrate a sample associativity calculation, which is
 representative of the general situation. Consider the following cells in H-Kl(X,T):
 J
 J
 α1
 α2
 β1
 α3
 γ
 J
 α4
 β2
 J
 J
 J
 J
 J
 There are two possible ways to compose these cells: either composing the bottom first:
 (γ(β1 ⊡β2))(α1 ⊡ α2 ⊡α3 ⊡α4)
 or the top two first, followed by composition with the bottom:
 γ((β1(α1 ⊡ α2)) ⊡ (β2(α3 ⊡ α4)))
 The first composite is given by the following composite in X:
 Tµ Tµ
 α1 Tα2
 β1
 T2α3
 µ
 ?
 ?
 ?
 ?
 ?
 ?
 ?
 T3α4
 ?
 µ
 Tβ2
 γ
 By using cell naturality of µ twice, the above becomes
 Tµ Tµ
 α1 Tα2
 β1
 µ µ
 Tα3
 J
 J
 J
 J
 J
 J
 T2α4
 Tβ2
 ?
 ?
 J
 J
 γ
23
 wethenusethemonadaxiomTµ◦µ=µ◦µtoget
 α1 Tα2
 µ µ
 µ µ
 β1
 Tα3 J J J J J J J J
 T2α4
 Tβ2
 γ
 whichisthesecondcompositeγ((β1(α1⊡α2))⊡(β2(α3⊡α4))).
 4.2. Remark.Unfortunately,wedonotknowofanyuniversalpropertysatisfiedbythis
 construction. Inparticular,H-Kl(X,T) isnotaKleisliobject forT invDbl inthesense
 of [Str72a];thelatterwouldinsteadcontainverticalKleisliarrows. Infact, forgeneralX
 thereneednotevenbeacanonical functorX H-Kl(X,T).
 Wecannowgiveourfirstpreliminarydefinitionofgeneralizedmulticategoriesrelative
 toamonadT.
 4.3. Definition.LetT beamonadonavirtual doublecategoryX. AT-monoidis
 definedtobeamonoidinH-Kl(X,T),andlikewiseforaT-monoidhomomorphism.
 WedenotethevirtualdoublecategoryMod(H-Kl(X,T)),whoseobjectsareT-monoids,by
 KMod(X,T).
 Asareference, thedata foraT-monoidconsistsofanobjectX0∈X, ahorizontal
 arrowX0
 X TX0 inX,andcells
 X0 TX0
 X0
 X0
 X0 T2X0 T2X0
 TX0
 µ
 X0 TX0 X
 X0 TX0
 X TX0 T2X0
 TX
 ¯ x and
 X0
 X0
 X0
 TX0
 η
 4 4 4 4 4 4 4
 X0 TX0 X
 ˆ x
 Notethatthesecellshavepreciselytheformswepredictedatthebeginningof§3.
 4.4. Remark.Wehave seen in§2 thatMod isa2-functor. In fact, under suitable
 hypotheses (involvingthenotionsof restrictionandcomposites tobe introduced in§5
 and§7),H-Kl isalsoa(pseudo) functor,andthussoisKMod. Infact,H-Kl isapseudo
 functor intwodifferentways, correspondingtothetwodifferentkindsofmorphismsof
 monads: laxandcolax. Thiswasobservedby[Lei04] inhiscontext;wewilldiscussthe
 functorialityofH-KlandKModinourframeworkintheforthcoming[CS10a].
 Wenowconsidersomeexamples.
24
 4.5. Example. Of course, if T is the identity monad on any X, then a T-monoid is just
 a monoid, and KMod(X,T) = Mod(X).
 Recall from Example 3.6 that any pullback-preserving monad C T C extends to a
 monad on Span(C).
 4.6. Example. If T is the “free monoid” monad extended to Span(Set) ∼ = Set-Mat,
 then a T-monoid consists of a set A0, a Set-matrix {A((x1,...,xn),y)}xi,y∈A0
 , and com
position and identity functions. It is easy to see that this reproduces the notion of an
 ordinary multicategory. Likewise, T-monoid homomorphisms are functors between multi
categories.
 4.7. Example. If T is the “free category” monad on directed graphs, then a T-monoid
 is a virtual double category. (This is, of course, the origin of the name “fc-multicategory,”
 where fc is a name for this monad.) The vertices and edges of the directed graph A0
 are the objects and horizontal arrows, respectively, while in the span A0 ← A → TA0
 the vertices of A are the vertical arrows and its edges are the cells. Likewise, T-monoid
 homomorphisms are functors between virtual double categories.
 4.8. Example. Let M be a monoid and T = (M ×−) the “free M-set” monoid on
 Span(Set). A T-monoid consists of a set A0 and a family of sets {A(m;x,y)}x,y∈A0,m∈M.
 The composition and identity functions make it into an M-graded category, i.e. a category
 in which every arrow is labeled by an element of M in a way respecting composition and
 identities. The case M = Z may be most familiar.
 4.9. Example. Let C be a lextensive category and T the monad (−)+1 on Span(C).
 A T-monoid consists of an object A0 and a span A0 ← A → A0 +1; since S is extensive,
 A decomposes into two spans A0 ← A1 → A0 and A0 ← B → 1. The composition and
 identity functions then make the first span into an internal category in C and the second
 into an internal diagram over this category.
 4.10. Example. Let S be a small category, and let T be the monad on Setob(S) whose
 algebras are functors S
 Set. Thus, for a family {Ax}x∈ob(S) in Setob(S) we have
 (TA)x =
 Ay ×S(x,y).
 y∈ob(S)
 This T preserves pullbacks, so it induces a monad on Span Setob(S) . A T-monoid
 A M TAcanbeidentified with a category over S, i.e a functor A
 S. Namely, the
 elements of the set Ax are the objects of the fiber of A over x ∈ ob(S), while M can be
 broken down into a collection of spans
 Ax
 Mx,y
 Ay ×S(x,y),
 which together supply the arrows of A and their images in S. The morphisms of T
monoids are likewise the functors over S.
25
 4.11. Example. If T is the “free strict ω-category” monad on Span(Globset), then
 a T-monoid of the form 1
 T1 can be identified with a globular operad in the sense
 of [Bat98], as described in [Lei04]. General T-monoids are globular multicategories (or
 many-sorted globular operads) as considered in [Lei04, p.273–274].
 Recall from Example 3.7 that any taut monad T on Set (such as the identity monad,
 the powerset monad, the filter monad, or the ultrafilter monad) extends to a monad on
 V-Mat for any completely distributive quantale V (such as 2 or R+). We will show
 in §B.6 that in such a case, our T-monoids are the same as the (T,V)-algebras studied
 by [CT03, CHT04, Sea05], and others; thus we have the following examples.
 4.12. Example. If T is the identity monad, then KMod(V-Mat,T) = V-Prof. Thus,
 for V = 2, T-monoids are preorders; and for V = R+, T-monoids are metric spaces (in
 the sense of [Law02]).
 4.13. Example. If T is the ultrafilter monad, and V = 2, then a T-monoid consists
 of a set equipped with a binary relation between ultrafilters and points satisfying unit
 and composition axioms. If we call this relation “convergence,” then the axioms precisely
 characterize the convergence relation in a topological space; thus T-monoids are topolog
ical spaces, and T-monoid homomorphisms are continuous functions. This observation is
 originally due to [Bar70] (note that although his construction of an ultrafilter monad on
 Rel looks quite different, it is in fact the same).
 4.14. Example. If T is the powerset monad, and V = 2, then T-monoids are closure
 spaces. A closure space consists of a set A equipped with an operation c(−) on subsets
 which is:
 • extensive: X ⊆ c(X),
 • monotone: Y ⊆ X ⇒c(Y)⊆c(X), and
 • idempotent: c(c(X)) ⊆ c(X).
 4.15. Example. If T is the ultrafilter monad and V = R+, then T-monoids are
 equivalent to approach spaces. An approach space is a set X equipped with a function
 d : X ×PX [0,∞]such that
 • d(x,{x}) = 0,
 • d(x,∅) = ∞,
 • d(x,A∪B) = min{d(x,A),d(x,B)}, and
 • ∀ǫ ≥0,d(x,A) ≤ d(x,{x : d(x,A) ≤ ǫ})+ǫ.
 Approach spaces have found applications in approximation theory, products of metric
 spaces, and measures of non-compactness: for more detail, see [Low88].
 Finally, we consider T-monoids relative to the additional examples of monads on
 V-Prof from the end of §3.
26
 4.16. Example. Let T be the “free symmetric strict monoidal V-category” monad on
 V-Prof from Example 3.14. If A0 is a discrete V-category, then a T-monoid A0
 A TA0
 is a symmetric V-enriched multicategory (known to some authors as simply a “multi
category”). Likewise, from the “free braided strict monoidal V-category” monad we
 obtain braided multicategories.
 If A0 is not discrete, then a T-monoid (for V = Set) is a symmetric multicategory in
 the sense of [BD98] and [Che04]: in addition to the multi-arrows, there is also another
 type of arrow between the objects of the multicategory which forms a category, and which
 acts on the multi-arrows.
 4.17. Example. Let T be the “free category with strictly associative finite products”
 monad on Set-Prof from Example 3.15. If A0 is a one-object discrete category, then a
 T-monoid A0
 A TA0 isaLawvere theory, as in [Law63]. If A0 has more than one object,
 but is still discrete, then a T-monoid A0
 A TA0 is a “multi-sorted” Lawvere theory.
 This is a little different from the more usual definition of Lawvere theory, but the
 equivalence between the two is easy to see. A Lawvere theory is commonly defined to
 be a category A with object set N such that each object n is the n-fold product 1n.
 This implies that A(m,n) ∼ = A(m,1)n, so it is equivalent to give just the collection of
 sets A(m,1) with suitable additional structure. Since T1 has object set N, a T-monoid
 1
 T1 also consists of sets A(m,1) for m ∈ N, and it is then straightforward to verify
 that the additional structures in the two cases are in bijective correspondence. Note,
 however, that the morphisms between such T-monoids do not correspond to all of the
 morphisms between theories considered in [Law63], but only those of “degree one;” the
 others are only visible from the “category with object set N” viewpoint.
 The relationship between these two definitions of Lawvere theory is analogous to the
 way in which an operad can also be defined as a certain sort of monoidal category with
 object set N. In fact, both arise from a very general adjunction between T-algebras and
 T-monoids; see Remark 9.16 and the forthcoming [CS10b].
 4.18. Example. If T is the “free V-category with strictly associative finite products”
 monad on V-Prof from Example 3.15 and A0 is a one-object discrete V-category, then
 a T-monoid A0
 A TA0 is a “V-enriched finite product theory.” If A0 is unchanged
 but T is instead the “free V-category with finitely presentable cotensors” monad from
 Example 3.16, then a T-monoid A0
 A TA0 isa“Lawvere V-theory”asdefined in [Pow99]
 (with the same caveat as in the previous example). To obtain a “multi-sorted Lawvere
 V-theory” we need T to adjoin both finite products and finite cotensors.
 4.19. Example. If T is any of
 • the “free symmetric strict monoidal category” monad,
 • the “free category with strictly associative finite products” monad, or
 • the “free category with strictly associative finite coproducts” monad,
27
 but now considered as a monad on Span(Cat), then a T-monoid with a discrete category
 of objects is a club in the sense of [Kel72b] and [Kel72a] (relative to P, S, or Sop, in
 Kelly’s terminology). See also §B.4.
 4.20. Remark. When T is the “free symmetric strict monoidal category” monad on
 Set-Prof, the horizontal arrows between discrete categories in H-Kl(Set-Prof,T) are the
 generalized species of structure of [FGHW08] (called structure types in [BD01]). The
 esp´eces de structures of [Joy81, Joy86] are the particular case of horizontal arrows 1
 1
 in H-Kl(Set-Prof,T). Likewise, when T is the analogous monad on Span(Gpd), the hor
izontal arrows in H-Kl(Span(Gpd),T) are the (generalized) stuff types of [BD01, Mor06].
 We can see from these examples that for virtual double categories whose objects are
 “category-like,” it is often the T-monoids whose objects are discrete which are of particular
 interest. We will make this notion precise in §8, and propose that often a better solution
 is to consider “normalized” T-monoids.
 First, however, we must develop some additional machinery for virtual double cate
gories. We will describe when horizontal arrows have units and composites, as well as
 when horizontal arrows can be “restricted” along vertical arrows. With this theory in
 hand, we can then return to study “object discrete” and “normalized” T-monoids, as well
 as when such T-monoids are “representable”.
 4.21. Remark.If V is a complete and cocomplete closed symmetric monoidal category,
 then the virtual double category V-Prof is itself “almost” of the form H-Kl(X,T). We take
 X to be the double category Sq(V-Cat), whose objects are V-categories, whose vertical
 and horizontal arrows are both V-functors, and whose cells are V-natural transformations,
 and we define TA = VAop to be the enriched presheaf category of A. The observation is
 then that a V-profunctor A B canbe identified with an ordinary V-functor A VBop,
 so that V-Prof is almost the same as H-Kl(Sq(V-Cat),T). This is not quite right, since
 T is not really a monad due to size issues. But these problems can be dealt with, for
 instance by using “small presheaves” as in [DL07].
 Assuming the functoriality of H-Kl mentioned in Remark 4.4, this observation implies
 that if S is another monad on V-Cat related to T by a distributive law, or equivalently a
 monad in the 2-category of monads and monad morphisms (see [Bec69, Str72b]), then S
 induces a monad on V-Prof, which we can in turn use to define generalized multicategories
 as S-monoids in V-Prof. For example, since a symmetric monoidal structure on A extends
 to TA by Day convolution, the “free symmetric monoidal V-category” monad distributes
 over T, inducing its extension to V-Prof considered in Example 3.14. This is the argument
 used in [FGHW08] to construct the bicategory H(H-Kl(V-Prof,T)). Similar arguments
 apply to the monad from Example 3.15.
 1. Composites and units
 In §2 we introduced (virtual) double categories as a framework in which one can define
 monoids and monoid homomorphisms so as to include both enriched and internal cate
28
 gories with the appropriate notions of functor. However, we would certainly like to be
 able to recover natural transformations as well, but this requires more structure than is
 present in a virtual double category.
 It is not hard to see that the vertical category of any (pseudo) double category can be
 enriched to a vertical 2-category, whose 2-cells f ⇒ g are the squares of the form
 A
 g
 B
 A
 f
 B,
 and that in examples such as Prof(C) and V-Prof these 2-cells recover the appropriate
 notion of natural transformation. In a virtual double category this definition is impossible,
 since there may not be any horizontal identity arrows. However, it turns out that we can
 characterize those horizontal identities which do exist by means of a universal property.
 In fact, it is not much harder to characterize arbitrary horizontal composites (viewing
 identities as 0-ary composites). In this section we study such composites; in the next
 section we will use them to define vertical 2-categories.
 5.1. Definition. In a virtual double category, a cell
 p1
 is said to be opcartesian if any cell
 r1
 f
 r2
 . . . rm
 p1
 factors through it uniquely as follows:
 r1
 r1
 f
 r2
 r2
 . . . rm
 ···
 . . . rm
 p1
 p2 ... pn
 ⇓opcart
 q
 p2 ... pn s1 s2 ... sk
 ⇓
 t
 p2 ... pn s1 s2 ... sk
 ⇓opcart
 q
 ⇓
 t
 g
 ···
 s1
 s2
 ... sk
 g
 .
 If a string of composable horizontal arrows is the source of some opcartesian cell, we
 say that it has a composite. We refer to the target q of that cell as a composite of the
 given string and write it as p1 ⊙ ··· ⊙ pn. Similarly, if n = 0 and there is an opcartesian
29
 cell of the form
 we say that X has a unit UX.
 X
 5
 5
 5
 5
 5
 5
 5
 5
 5
 5
 ⇓ 5 5 5
 5
 5
 5
 X UX
 X.
 These universal properties make it easy to show that composites and units, when
 they exist, behave like composites and units in a pseudo double category. For example,
 composites and units are unique up to isomorphism: given two opcartesian arrows with
 the same source, factoring each through the other gives an isomorphism between their
 targets. Likewise, the composite of opcartesian cells is opcartesian, so composition is
 associative up to coherent isomorphism whenever all relevant composites exist. More
 precisely, if p ⊙ q exists, then (p ⊙q) ⊙r exists if and only if p⊙q ⊙r exists, and in that
 case they are isomorphic. It follows that if p ⊙ q and q ⊙r exist, then
 (p ⊙q)⊙r ∼ = p⊙(q⊙r),
 each existing if the other does. Similarly, any string in which all but one arrow is a unit:
 X UX ... UX X p Y UY ... UY Y
 has a composite, which is (isomorphic to) p.
 The following theorem, which was also observed in [DPP06], is a straightforward gen
eralization of the relationship between monoidal categories and ordinary multicategories
 described in [Her00]. It is also a special case of the general relationship between pseudo
 algebras and generalized multicategories, as in [Lei04, §6.6], [Her01], and §9 of the present
 paper.
 5.2. Theorem.A virtual double category is a pseudo double category if and only if every
 string of composable horizontal arrows (including zero-length ones) has a composite.
 Proof (sketch). “Only if” is clear, by definition of how a pseudo double category
 becomes a virtual one. For “if”, we use the isomorphisms constructed above; we invoke
 again the universal property of opcartesian cells to show coherence.
 5.3. Example. If V has an initial object ∅ which is preserved by ⊗ on both sides, then
 V-Mat has units: the unit of a set X is the matrix
 UX(x,x′) = I x=x′
 ∅ x=x′.
 If V has all small coproducts which are preserved by ⊗ on both sides, then V-Mat has
 composites given by “matrix multiplication.” For instance, the composite of matrices
 X p Y andY q Zis
 (p ⊙q)(z,x) =
 p(y, x) ⊗ q(z,y).
 y∈Y
30
 5.4. Example.SinceSpan(C) isapseudodoublecategory, all compositesandunits
 always exist. Composites are givenbypullback, and theunit ofX is theunit span
 X←X→X.
 RegardingunitsinV-ProfandProf(C),wehavethefollowing.
 5.5. Proposition.Foranyvirtual doublecategoryX,allunitsexist inMod(X). For
 anymonoidA, itsunitcell
 A0 A0 A
 A0
 A0
 ••••••••
 ••••••••
 A0
 A0
 ? ? ? ? ? ? ? ?
 ? ? ? ? ? ? ? ?
 A0 A0 |
 ⇓ˆa
 isopcartesianinMod(X).Therefore,UAisAitself,regardedasanA-A-bimodule.
 Proof.Firstly, theunitaxiomsofAshowthatˆais, infact,acell inMod(X).Nowwe
 mustshowthatcomposingwithˆagivesabijectionbetweencells
 D E P
 B
 D
 g
 B CC
 E
 f
 B A p1...pm_ _ _ _ _ A C q1...qn _ _ _ _ _
 ⇓α and
 D E p
 B
 D
 g
 B CC
 E
 f
 B A p1...pm_ _ _ _ _ A A AA C q1...qn _ _ _ _ _
 ⇓β
 inMod(X).Clearlycomposinganycellβofthesecondformwithˆagivesacellαofthe
 first form. Conversely, givenαof thefirst form, therearetwocellsof thesecondform
 definedbylettingAactfirstonpmfromtherightandq1fromtheleft,respectively.These
 areequalbyoneof theaxioms forαtobeacell inMod(X);we letβbetheircommon
 value. (Inthecasewhenm=0orn=0,weusetheactionofforginstead.)Theother
 axiomsforαthencarryovertoβtoshowthatit isacell inMod(X).
 TheunitaxiomsfortheactionofAonbimodulesshowthatα→β→αistheidentity,
 whiletheequivarianceaxiomsforβregardingthetwoactionsofAshowthatβ→α→β
 istheidentity.Thuswehaveabijection,asdesired.
 Therefore, sinceV-Prof=Mod(V-Mat)andProf(C)=Mod(Span(C)), theyboth
 alwayshaveallunits. Bycontrast, extraassumptionsonXarerequiredforcomposites
 toexist inMod(X);herearethetwoexamplesofgreatest interesttous.
 5.6. Example.IfVhassmallcolimitspreservedby⊗onbothsides, thenV-Profhas
 allcomposites; thecompositeofenrichedprofunctorsA p BandB q Cisgivenby
 thecoend
 (p⊙q)(z,x)= y∈B
 p(y,x)⊗q(z,y).
31
 5.7. Example. If C has coequalizers preserved by pullback, then Prof(C) has all com
posites; the composite of internal profunctors is an “internal coend.”
 Together with Proposition 5.5, these examples will suffice for the moment. In appendix
 A we will give general sufficient conditions for composites to exist in Mod(X), and for
 composites and units to exist in H-Kl(X,T).
 5.8. Remark. If Definition 5.1 is satisfied only for m = k = 0, we say that the cell is
 weakly opcartesian. We do not regard a weakly opcartesian cell as exhibiting its target
 as a composite of its source, since the weak condition is insufficient to prove associativity
 and unitality. However, a weakly opcartesian cell does suffice to detect its target as the
 composite of its source, if we already know that that composite exists. Furthermore, if
 any composable string in X is the source of a weakly opcartesian cell and moreover weakly
 opcartesian cells are closed under composition, then one can show, as in [Her00], that in
 fact every weakly opcartesian cell is cartesian; see also §9.
 Virtual double categories having only weakly opcartesian cells seem to be fairly rare;
 one example is V-Mat where V has colimits which are not preserved by its tensor product.
 Note that in this case, V-Prof need not even have weakly opcartesian cells, since we
 require ⊗ to preserve coequalizers simply to make the composite of two profunctors into
 a profunctor.
 If X and Y have units, we say that a functor (or monad) X F Y is normal if it
 preserves opcartesian cells with nullary source, which is to say it preserves units in a
 coherent way. Likewise, if X and Y have all units and composites (i.e. are pseudo double
 categories), we say that X F Y is strong if it preserves all opcartesian cells.
 5.9. Example. Any functor Span(C)
 functor C
 Span(D) induced by a pullback-preserving
 Dis strong, and in particular normal.
 5.10. Example. It is also easy to see that Mod(F) is normal for any functor F, by the
 construction of units in Proposition 5.5.
 5.11. Examples. If V is a cocomplete symmetric monoidal category in which ⊗ pre
serves colimits on both sides, then V-Mat has all composites, and the extension of the
 “free monoid” monad to V-Mat from Example 3.12 is easily seen to be strong. Since
 the “free strict monoidal V-category” monad on V-Prof is obtained by applying Mod
 to this, it is normal by our above observation. In fact, it is also strong, essentially be
cause the tensor product of reflexive coequalizers is again a reflexive coequalizer (see, for
 example, [Joh02, A1.2.12]).
 5.12. Examples. The “free symmetric strict monoidal V-category” monad on V-Prof
 from Example 3.14 is also normal, essentially by definition, as are the “free V-category
 with strictly associative finite products” monad from Example 3.15 and its relatives from
 Example 3.16. A more involved computation with coequalizers shows that the first is
 actually strong, and the second is strong whenever V is cartesian monoidal. However, it
 seems that the others are not in general strong.
32
 5.13. Examples. The monads on V-Mat constructed in Example 3.7 are not generally
 strong or even normal. Two notable exceptions are the ultrafilter monads on Rel and
 R+-Mat, of which the first is strong and the second is normal.
 We write vDbln for the locally full sub-2-category of vDbl determined by the virtual
 double categories with units and normal functors between them; thus Mod is a 2-functor
 vDbl
 vDbln. In fact, we have the following.
 5.14. Proposition.Mod is right pseudo-adjoint to the forgetful 2-functor vDbln
 vDbl.
 Proof. “Pseudo-adjoint” means that we have a pseudonatural η and ǫ that satisfy the
 triangle identities up to coherent isomorphism. We take ǫX to be the forgetful functor
 Mod(X)
 X which sends a monoid to its underlying object and a module to its un
derlying horizontal arrow; this is strictly 2-natural. If X has units, we take ηX to be
 the “unit assigning” functor X
 Mod(X) which sends X to UX (which has a unique
 monoid structure) and X p Y to itself considered as a (UX,UY)-bimodule; this is only
 pseudonatural since normal functors preserve units only up to isomorphism. But if we
 choose the units in Mod(X) according to Proposition 5.5, then the triangle identities are
 satisfied on the nose.
 In particular, if 1 denotes the terminal virtual double category, then the category
 of normal functors 1
 X is equivalent to the vertical category of X. It then follows
 from Proposition 5.14 that the category of arbitrary functors 1
 X is equivalent to the
 vertical category of Mod(X). Thus, Proposition 5.14 generalizes the well-known observa
tion (which dates back to [B´en67]) that monoids in a bicategory B are equivalent to lax
 functors 1
 B.
 5.15. Remark. It follows that Mod is a pseudomonad on the 2-category vDbln, and so
 in particular it has a multiplication
 Mod(Mod(X))
 Mod(X).
 (5.16)
 Inspection reveals that an object of Mod(Mod(X)) consists of an object X of X, two
 monoids X A X andX M X,andamonoidhomomorphism A M whose vertical
 arrow components are identities. The multiplication (5.16) simply forgets the monoid A.
 This idea will be further discussed in [CS10b].
 5.17. Remark.If X is a virtual double category in which all units and composites exist
 (equivalently, it is a pseudo double category), then it has a horizontal bicategory H(X)
 consisting of its objects, horizontal arrows, and cells of the form
 ⇓
 .
 Clearly when C and V satisfy the required conditions for all composites to exist in our
 examples, we recover in this way the usual bicategories of matrices, spans, and enriched
33
 and internal profunctors. Any functor between pseudo double categories likewise induces
 a lax functor of horizontal bicategories, but this is not true of transformations without
 additional assumptions; see Remarks 7.26 and A.5.
 1. 2-categories of T-monoids
 As proposed in the previous section, we now use the notion of units introduced there to de
f
 ine 2-categories of generalized multicategories, generalizing the approach taken in [Lei04,
 §5.3].
 6.1. Proposition. Let X be a virtual double category in which all units exist. Then it
 has a vertical 2-category VX whose objects are those of X, whose morphisms are the
 f
 vertical arrows of X, and whose 2-cells A
 g
 α B are the cells
 g
 A UA
 ⇓α
 A
 f
 B UB
 B
 in X.
 Proof. This is straightforward; note that when composing 2-cells we must use the iso
morphisms UA 
∼ = UA ⊙UA.
 In particular, for any X, Mod(X) has a vertical 2-category, which we denote Mon(X)
 and call the 2-category of monoids in X. (This 2-category is closely related to various
 2-categories of monads in a bicategory; see [LS02, §2.3–2.4].) It turns out that in this
 case, the description of the 2-cells of Mon(X) can be rephrased in a way that looks much
 more like a natural transformation.
 f
 6.2. Proposition. Giving a 2-cell A
 g
 α B in Mon(X) is equivalent to giving a cell
 ••••••••
 A0
 A0
 g0
 ?
 ?
 ?
 ⇓α0
 B0
 B0
 B0
 |
 ?
 ?
 ?
 f0
 ?
 ?
 B0
 B0
 B0
 B
34
 inXsuchthat
 B0 B0 B
 A0
 B0
 f0
 A0 A0
 A A0
 B0
 f0 ⇓f
 A0
 B0
 g0
 •••••••••
 α0
 ⇓
 B0 B0 B
 ⇓¯ b
 B0 B0 B
 B0
 B0
 B0 B0 B0
 B0
 = B0 B0 B
 A0
 B0
 g0
 A0 A0
 A A0
 B0
 g0 g⇓
 A0
 B0
 f0
 ? ? ? ? ? ? ? ? ?
 ⇓α0
 B0 B0 B
 ⇓¯ b
 B0 B0. B
 B0
 B0
 B0 B0 B0
 B0.
 (6.3)
 Proof.This isan instanceofProposition5.5,wherem=n=0, f=g=1A, and
 P=UA.
 6.4. Example.Recall thatinV-Prof=Mod(V-Mat),theobjectsareV-enrichedcat
egoriesandtheverticalmorphismsareV-enrichedfunctors; thus thesearetheobjects
 andmorphismsofMon(V-Mat). Recalling fromExample2.6thedefinitionof cells in
 V-Mat,Proposition6.2 implies thata2-cell A
 f
 g
 αB inMon(V-Mat) isgivenbya
 familyofmorphismsI αx B(fx,gx) forxanobjectofA, suchthat foreveryx,ythe
 followingsquarecommutes:
 B(gx,gy)⊗B(fx,gx) B(fx,gy).
 A(x,y)
 B(gx,gy)⊗B(fx,gx)
 g⊗αx
 A(x,y) B(fy,gy)⊗B(fx,fy) αy⊗f B(fy,gy)⊗B(fx,fy)
 B(fx,gy).
 ThisispreciselytheusualdefinitionofaV-enrichednaturaltransformation;thuswehave
 Mon(V-Mat)≃V-Cat.
 6.5. Example.Likewise,Mon(Span(C))≃Cat(C) isthe2-categoryof internal cate
gories, functors,andnaturaltransformationsinC.
 6.6. Examples.Ontheotherhand, thevertical 2-categoryofSpan(S) is justS, re
gardedasa2-categorywithonlyidentity2-cells. Thevertical 2-categoryofV-Matde
pends onwhatVis, butusually it isnotvery interesting. Thus, ingeneral, vertical
 2-categoriesareonlyinterestingforvirtualdoublecategorieswhoseobjectsare“category
like”ratherthan“set-like.”
 Now, ifT isamonadonavirtualdoublecategoryX,wewriteKMon(X,T) forthe
 2-categoryV(KMod(X,T))andcall itthe2-categoryofT-monoids inX. Itsobjectsare
 T-monoids, itsmorphismsareT-monoidhomomorphisms,andits2-cellsmaybecalledT
monoidtransformations.ByProposition6.2andthedefinitionofH-Kl(X,T),aT-monoid
35
 transformationα:f g:A Bisspecifiedbyacell
 B0 TB0 B
 A0
 B0
 g0
 ••••••••
 A0
 TB0
 Tf0◦ηA0=ηTB0◦f0
 ? ? ? ? ? ? ? ?
 B0 TB0 |
 ⇓α0
 suchthat
 TA0 T2A0 B
 A0
 TA0
 η
 A0 TA0
 A TA0
 T2A0
 η ⇓ηA
 TB0 T2B0 TB
 TA0
 TB0
 Tf0
 TA0 T2A0 T2A0
 T2B0
 T2f0 ⇓Tf
 A0
 B0
 g0
 α0
 ⇓
 B0 TB0 B
 ⇓¯ b
 B0 TB0 B
 B0
 B0
 B0 T2B0 T2B0
 TB0
 µB
 = B0 TB0 B
 A0
 B0
 g0
 A0 TA0
 A TA0
 TB0
 Tg0 g⇓
 TA0
 T2B0
 T(ηB0)◦Tf0
 ⇓Tα0
 TB0 T2B0 TB
 ⇓¯ b
 B0 TB0. B
 B0
 B0
 B0 T2B0 T2B0
 TB0.
 µB
 Manyauthorshavedefinedthis2-categoryKMon(X,T)inseeminglyad-hocways,whereas
 it fallsquitenaturallyoutof the frameworkofvirtualdoublecategories. Thiswasalso
 observedin[Lei04,§5.3]; see§B.1.
 6.7. Example.LetT be the“freemonoid”monadonSet-Mat, so thatT-monoids
 areordinarymulticategories. IfA f
 g
 Bare functors, thenaccordingtotheabove, a
 transformationf α gconsistsof, foreachx∈A,amorphismαx∈B(η(fx),gx)(that
 istosay,amorphism(fx) αx gxwithsourceoflengthone)suchthatforanymorphism
 ξ: (x1,...,xn) yinA,wehave
 αy◦f(ξ)=g(ξ)◦(αx1
 ,...,αxn
 ).
 This istheusualnotionoftransformationforfunctorsbetweenmulticategories.
 6.8. Example.WhenT is the“freecategory”monadondirectedgraphs, sothatT
monoids arevirtual double categories, T-monoidtransformations are the sameas the
 transformationswedefinedin3.1.
 6.9. Example.LetUbetheultrafiltermonadonRel,sothatU-monoidsaretopological
 spaces. IfA f
 g
 Barecontinuousmaps (i.e.U-monoidhomomorphisms), thenthere
 existsatransformationf g(whichisnecessarilyunique) justwhenforallx∈A, the
 principalultrafilterηfxconvergestogxinB. This isequivalenttosayingthatf≥g in
36
 the pointwise ordering induced by the usual specialization order on B. The situation for
 other topological examples is similar.
 Any normal functor clearly induces a strict 2-functor between vertical 2-categories. In
 fact, if 2-Cat denotes the 2-category of 2-categories, strict 2-functors, and strict 2-natural
 transformations, then we have:
 6.10. Proposition. There is a strict 2-functor V: vDbln
 2-Cat.
 In particular, any normal monad T on X induces a strict 2-monad on V(X). As we saw
 in §3, most monads on virtual double categories are “extensions” of a known monad on
 their vertical categories (or vertical 2-categories), so this construction usually just recovers
 the familiar monad we started with. In §9, we will show that V(T)-algebras are closely
 related to T-monoids.
 1. Virtual equipments
 If we have succeeded in convincing the reader that virtual double categories are inevitable,
 she may be justified in wondering why they have not been more studied. Certainly,
 virtual double categories involve significant complexity above and beyond pseudo double
 categories, and the latter suffice to describe the important examples Span(C), V-Mat,
 V-Prof, and Prof(C) as long as V and C are suitably cocomplete. However, even pseudo
 double categories have generally received less publicity than bicategories.
 One possible reason for this is that in most of the (pseudo or virtual) double categories
 arising in practice, the vertical arrows are more tightly coupled to the horizontal arrows
 that we have heretofore accounted for; in fact they can almost be identified with certain
 horizontal arrows. For example, a V-functor A f B is determined, up to isomorphism,
 by the V-profunctor A B(1,f) B defined by B(1,f)(b,a) = B(b,fa). Furthermore, this
 coupling is very important for many applications, such as the formal definition of weighted
 limits and colimits (see [Str83, Woo82]), so a mere double category (pseudo or virtual)
 would be insufficient for these purposes. Because of this, many authors have been content
 to work with bicategories, or bicategories with a collection of horizontal arrows singled
 out (such as the “proarrow equipments” of [Woo82]).
 However, while not all pseudo double categories exhibit this type of coupling, it is
 possible to characterize those that do (and they turn out to be equivalent to the “proarrow
 equipments” mentioned above). The basic idea of this dates back to [BS76], but it has
 recently been revived in various equivalent forms; see for instance [Ver92, GP99, GP04,
 DPP07, Shu08] and the Notes at the end of [Lei04, Ch. 5]. Since this type of coupling
 also plays an important role in the theory of generalized multicategories, in this section
 we give the basic definitions appropriate to the virtual case.
 The basic idea is the following. The profunctor B(1,f) considered above can be
 constructed in two stages: first we consider the hom-profunctor B(−,−): B
 B, and
 then we precompose it with f on one side. We already know from §5 that hom-profunctors
37
 are the units in V-Prof, so it remains only to characterize precomposition with functors
 in terms of V-Prof. This is accomplished by the following definition.
 7.1. Definition. A cell
 p
 f ⇓cart g
 q
 in a virtual double category is cartesian if any cell
 r1
 fh
 factors through it uniquely as follows:
 r1
 h
 f
 r2
 ⇓
 q
 r2
 ⇓
 . . . rn
 . . . rn
 p
 ⇓cart
 q
 (7.2)
 gk
 k
 g
 .
 If there exists a cartesian cell (7.2), we say that the p is the restriction q(g,f). The
 notation is intended to suggest precomposition of a profunctor q(−,−) with f and g.
 When f or g is an identity, we write q(g,1) or q(1,f), respectively. It is evident from the
 universal property that restrictions are unique up to isomorphism, and pseudofunctorial;
 that is, we have q(1,1) ∼
 =q and q(1,g)(1,f) ∼ = q(1,gf) coherently.
 We say that X has restrictions if q(g,f) exists for all q, f, and g, and that a functor
 preserves restrictions if it takes cartesian cells to cartesian cells. We write vDblr for
 the sub-2-category of vDbl determined by the virtual double categories with restrictions
 and the restriction-preserving functors.
 7.3. Examples. The virtual double categories V-Mat, V-Prof, Span(C), and Prof(C)
 have all restrictions. Restrictions in V-Mat are given by reindexing matrices, restrictions
 in Span(C) are given by pullback, and restrictions in V-Prof and Prof(C) are given by
 precomposing with functors.
 Note that the restrictions in V-Prof and Prof(C) are induced by those in V-Mat and
 Span(C), in the following general way.
 7.4. Proposition. If X is a virtual double category with restrictions, then Mod(X) also
 has restrictions.
38
 Proof. If B p D is a bimodule in X and
 f0
 A0
 A
 ⇓f
 A0
 f0
 B0 B
 B0
 and
 C0
 g0
 C0
 C
 ⇓g
 g0
 D0 D
 D0
 are monoid homomorphisms, then the restriction p(g0,f0) in X becomes an (A,C)-bimodule
 in an obvious way, making it into the restriction p(g,f) in Mod(X).
 The other ingredient in the construction of generalized multicategories also preserves
 restrictions.
 7.5. Proposition. If X is a virtual double category with restrictions and T is a monad
 on X, then H-Kl(X,T) also has restrictions.
 Proof. Let A p TB beahorizontal arrow in X, regarded as a horizontal arrow A B
 in H-Kl(X,T). It is easy to verify that the restriction of p along C f A and D g B
 in H-Kl(X,T) is given by the restriction p(Tg,f) in X.
 Therefore, if X has restrictions, so does KMod(X,T) for any monad T on X. Moreover,
 by Proposition 5.5, KMod(X,T) always also has units. As suggested in the introduction
 to this section, units and restrictions together are an especially important combination,
 so we give a special name to this situation.
 7.6. Definition. A virtual equipment is a virtual double category in which all units
 and all restrictions exist.
 We write vEquip for the locally full sub-2-category of vDbl determined by the virtual
 equipments and the normal restriction-preserving functors between them (however, see
 Theorem 7.24). We can now observe that Mod is a 2-functor from vDblr to vEquip.
 7.7. Examples. Span(C), V-Prof, and Prof(C) are always virtual equipments, and
 V-Mat is a virtual equipment whenever V has an initial object preserved by ⊗. More
 generally, Mod(X) and KMod(X,T) are virtual equipments whenever X has restrictions.
 If A f B is a vertical arrow in a virtual equipment, we define its base change
 objects to be
 B(1,f) = UB(1,f)
 These come with cartesian cells
 f
 B(1,f)
 UB
 and
 and
 B(f,1) = UB(f,1).
 B(f,1)
 f
 .
 (7.8)
 UB
39
 ByfactoringUf throughthesecartesiancells,weobtaintwofurthercells
 UA
 f
 B(f,1)
 and
 UA
 f
 B(1,f)
 (7.9)
 suchthatthefollowingequationshold:
 UA
 f
 B(1,f)
 f
 UB
 =
 UA
 f ⇓Uf f
 UB
 UA
 f
 B(f,1)
 f
 UB
 =
 UA
 f ⇓Uf f
 UB
 (7.10)
 Moreover, thefollowingequationsalsohold:
 UA B(1,f)
 f
 B(1,f) UB
 B(1,f)
 ⇓opcart
 =
 UA
 ⇓opcart
 B(1,f)
 B(1,f)
 (7.11)
 B(f,1) UA
 f
 UB B(f,1)
 B(f,1)
 ⇓opcart
 =
 B(f,1)
 ⇓opcart
 UA
 B(f,1)
 (7.12)
 Wecanverifythesebypostcomposingeachsidewiththeappropriatecartesiancell,using
 the equations (7.10), and invoking theuniqueness of factorizations throughcartesian
 cells. Inthe terminologyof [DPP07], equations (7.10)–(7.12)aresaidtomakeB(1,f)
 andB(f,1)intoacompanionandaconjointoff, respectively.
 7.13. Example.InSpan(C),thebasechangeobjectsB(1,f)andB(f,1)arethespans
 A
 A
 1A
 A
 B
 f < < < < <
 and
 A
 B
 f
 A
 A
 1A < < < < <
 respectively.Theseareoftencalledthegraphoff.
40
 7.14. Example. In V-Mat, for a function f: X
 is the matrix
 Y the base change object Y(1,f)
 Y(1,f)(x,y) = I if f(x) = y
 ∅ otherwise.
 7.15. Example. In V-Prof, the base change objects B(1,f) and B(f,1) are the rep
resentable distributors defined by B(1,f)(b,a) = B(b,fa) and B(f,1)(a,b) = B(fa,b).
 Base change objects in Prof(C) are analogous.
 At first glance, base change objects may seem only to be a particular special case of
 restrictions. However, it turns out that all restrictions can be recovered by composition
 with the base change objects (hence the name).
 7.16. Theorem. Let B p D be a horizontal arrow and f: A B and g: C D be
 vertical arrows in a virtual equipment. Then B(1,f)⊙p⊙D(g,1) exists and is isomorphic
 to p(g,f).
 Proof. Consider the composite
 B(1,f)
 f
 UB
 p
 1p
 p
 ⇓opcart
 p
 Dg
 UD
 g
 (7.17)
 By the universal property of restriction, this factors through the cartesian cell defining
 p(g, f) to give a canonical cell
 B(1,f)
 p
 p(g,f)
 D(g,1)
 We claim that this cell is opcartesian. To show this, suppose given a cell
 _
 h
 _
 _
 B(1,f)
 p
 q
 D(g,1)
 _
 _
 _
 k
 .
 (7.18)
 .
41
 Weneedtofactorituniquelythrough(7.18).Afactorizationisgivenbythecomposite
 _ _ _ _ _
 ssssssssss
 ssssssssss p(g,f)
 ssssssssss
 ssssssssss _ _ _ _ _
 K K K K K K K K K K
 K K K K K K K K K K
 L L L L L L L L L L L
 L L L L L L L L L L L
 _ _ _ _ _ UA
 f
 p(g,f)
 g
 UC
 _ _ _ _ _
 h
 _ _ _ _ _ B(1,f) p D(g,1) _ _ _ _ _
 k
 q
 .
 Toverifythatthis isafactorization,andthat it isunique,weusetheequations(7.10)
(7.12).Thedetailsaresimilartotheproofof [Shu08,Theorem4.1].
 7.19. Corollary.For vertical arrows f:A Band g:B C, the composite
 B(1,f)⊙C(1,g)alwaysexistsandisisomorphictoC(1,gf),anddually.
 Wealsohavethefollowingdualresult.
 7.20. Theorem.Forarrowsf:A Bandg:C Dinavirtual equipment,we
 haveabijectionbetweencellsof theform
 A p
 f
 C
 g
 B q D
 and
 BB(f,1)A p CD(1,g)D
 B q D
 Proof.The inversebijections aregivenbycomposingwiththe cells (7.8) and(7.9).
 (Recallthatallcompositeswithunitsexistinanyvirtualdoublecategory.)Thefactthat
 theyareinverses followsfrom(7.10)–(7.12).
 ItfollowsthatinthesituationofTheorem7.20, ifthecompositeB(f,1)⊙p⊙D(1,g)
 exists, thenit isa“corestriction”or“extension”ofpalongfandg—that is, itsatisfies
 auniversalpropertydual tothatofarestriction.
 CombiningTheorems7.16and7.20,weobtainthefollowing.
 7.21. Corollary.Inavirtualequipment, thereisabijectionbetweencellsoftheform
 p
 h
 B(1,f)
 k
 D(1,g) q
 and
 p
 h f
 g k
 q
 Takingpandqtobeunitsandhandktobeidentities,weobtain:
42
 7.22. Corollary. For vertical arrows f,g: A
 a bijection between cells f
 g in VX and cells
 B(1,f)
 ⇓
 ,
 B(1,g)
 B(f,1).
 B in a virtual equipment X, there is
 which respects composition. Similarly, we have a bijection between cells f
 B(g,1)
 g and cells
 Now suppose that X is a virtual equipment which moreover has all composites. Then
 it has a horizontal bicategory HX, and Corollaries 7.19 and 7.22 imply that f → B(1,f)
 defines a pseudofunctor VX
 HX which is locally full and faithful. Furthermore, it is
 easy to verify that B(f,1) is right adjoint to B(1,f) in HX.
 This structure—a pseudofunctor which is bijective on objects, locally full and faithful,
 and which takes each 1-cell to one having a right adjoint—was defined in [Woo82] to
 constitute an equipment. This is the structure we referred to in the introduction to
 this section, which many authors have used where we would find double categories more
 natural. In fact, it is not hard to show (see [Shu08, Appendix C]) that an equipment in
 the sense of [Woo82] is equivalent to a virtual equipment which has all composites (this
 was called a framed bicategory in [Shu08]). Therefore, from now on we use equipment
 to mean a virtual equipment having all composites (thereby justifying the terminology
 “virtual equipment”).
 7.23. Remark. It was shown in [Shu08] that an equipment can equally well be defined
 as a pseudo double category in which all restrictions exist, or in which all “extensions”
 exist (in the sense mentioned after Theorem 7.20), or in which there exist base change
 objects with cells (7.8) and (7.9) satisfying (7.10)–(7.12). In the virtual case, we have a
 Goldilocks trifurcation: merely having base change objects is too weak, and having all
 extensions is too strong, but having restrictions (together with units) is just right.
 We now consider how functors and transformations interact with restrictions.
 7.24. Theorem. Any functor F between virtual equipments preserves restriction.
 Proof.Theproofgiven for equipments in [Shu08, Theorem 6.4] applies basically verbatim
 to virtual equipments.
 In particular, vEquip is in fact a full sub-2-category of vDbln. Note, though, that an
 arbitrary functor F between virtual equipments still may not preserve units, so that while
 we have F(B(1,f)) ∼ = FUB(1,Ff), neither need be the same as FB(1,Ff). Of course,
 they are the same if F is normal.
 F
 Now, recall that any transformation X
 G
 α Y of functors between virtual equip
ments induces a strictly 2-natural transformation V(α) of 2-functors between vertical 2
categories. In particular, we have αB◦F(f) = G(f)◦αA for any vertical arrow f : A
 B
43
 in X. However, we also have the cell component
 F(B(1,f))
 αA ⇓αB(1,f) αB
 G(B(1,f))
 of α. If F and G are normal, so that F(B(1,f)) ∼ = FB(1,Ff) and G(B(1,f)) ∼ =
 GB(1,Gf), then by Corollary 7.21, αB(1,f) induces a 2-cell αB ◦ F(f)
 G(f) ◦ αA,
 which seems to be trying to make V(α) into an oplax natural transformation. Fortu
nately, however, this is an illusion.
 7.25. Proposition. In the above situation, the 2-cell αB ◦F(f)
 by αB(1,f) is an identity.
 G(f)◦αA induced
 Proof. This follows by inspection of how this 2-cell is constructed, and use of the cell
 naturality of α.
 7.26. Remark. Recall from Remark 5.17 that any functor X F Y between pseudo
 double categories induces a lax functor H(X) H(F) H(Y) between horizontal bicate
gories, but not every transformation F
 G induces a transformation H(F)
 H(G).
 It is true, however, that if X and Y are equipments, then any transformation F α G
 induces an oplax transformation H(F) H(α) H(G) whose component at X is GX(1,αX).
 Likewise, the components (GX)(αX,1) form a lax transformation H(G)
 H(F). See
 also Remark A.5.
 1. Normalization
 With the notion of virtual equipment under our belt, we now return to the general theory
 of generalized multicategories. We observed in §4 that for virtual double categories whose
 objects are “category-like,” such as V-Prof and Prof(C) (as opposed to those such as
 V-Mat and Span(C), whose objects are “set-like”), general T-monoids often contain too
 much structure. For instance, if T is the “free strict monoidal category” monad on
 Set-Prof, then a T-monoid consists of a category A, a multicategory M and a bijective
on-objects functor from A to the underlying category of M. Usually, the morphisms of
 A constitute superfluous data which we would like to eliminate. (This is not always true,
 though: in [Che04] these extra morphisms played an important role.)
 The obvious way to eliminate this extra data, which we adopted in describing examples
 of this sort in §4, is to require A to be a discrete category; this way the extra morphisms
 simply do not exist. However, a different way to eliminate it is to require the given functor
 A Mtoinduceanisomorphism between A and the underlying category of M; this way
 the extra morphisms exist, but are determined uniquely by the rest of the structure. In
 this section we define general analogues of both approaches, show their equivalence under
44
 general hypotheses, and argue that when they are not equivalent it is usually the second
 approach that is more useful. (This second approach was also the one taken in [Her01].)
 8.1. Definition. Let X be a virtual equipment and let T be a monad on Mod(X). A
 T-monoid A M TA is called object-discrete if A is a monoid in X of the form UX.
 We write dKMod(Mod(X),T) for the full sub-virtual-equipment of KMod(Mod(X),T)
 determined by the object-discrete T-monoids, and dKMon(X,T) for its vertical 2-category.
 Note that object-discreteness is only defined for a monad on a virtual equipment of the
 form Mod(X).
 8.2. Definition. Let T be a monad on a virtual equipment X. A T-monoid A M TA
 is normalized if its unit cell
 A UA A
 η
 A M
 TA
 is cartesian in X.
 We write nKMod(X,T) for the full sub-virtual-equipment of KMod(X,T) determined
 by the normalized T-monoids, and nKMon(X,T) for its vertical 2-category. Unlike object
discreteness, normalization is defined for monads on any virtual equipment.
 Now, to prove an equivalence between normalization and object-discreteness, we need
 to introduce the following definitions.
 8.3. Definition. A monoid homomorphism
 A0
 A0
 f0
 B0
 B0
 A A0
 f
 f
 A0
 f0
 B0
 B0
 in a virtual double category X is called bijective on objects (or b.o.) if f0 is an iso
morphism. It is called fully faithful (or f.f.) if the cell f is cartesian.
 8.4. Lemma. If A0
 A A0 is a monoid in a virtual double category X with restrictions
 and X f A0 is any vertical arrow, then X A(f,f) X is also a monoid, and its defining
 cartesian cell is a monoid homomorphism with f as its vertical part.
 Proof. To obtain a multiplication for A(f,f), we compose two copies of the defining
 cartesian cell with the multiplication of A, then factor the result through the defining
 cartesian cell. The unit is similar.
45
 8.5. Lemma. If X has restrictions, then (b.o., f.f.) is a factorization system on the
 category Mon(X) of monoids and monoid homomorphisms in X.
 Proof. Orthogonality is supplied by the universal property of cartesian cells, together
 with the fact that isomorphisms are orthogonal to anything. Factorizations are given by
 restriction along the vertical arrow component of a monoid homomorphism, using the
 previous lemma.
 8.6. Theorem. Let X be a virtual equipment, and let T be a monad on Mod(X) which
 preserves b.o. morphisms. Then
 (i) dKMod(Mod(X),T) is coreflective in KMod(Mod(X),T) (that is, its inclusion has
 a right adjoint in vEquip),
 (ii) nKMod(Mod(X),T) is reflective in KMod(Mod(X),T), and
 (iii) the induced adjunction
 dKMod(Mod(X),T)
 is an adjoint equivalence.
 nKMod(Mod(X),T)
 Proof. We first prove (i). Let A M TA be a T-monoid in Mod(X), where A0
 A A0 is
 a monoid in X. The unit of A is a monoid homomorphism e: UA0
 M(Te,e): UA0
 A, so by Lemma 8.4,
 T(UA0
 ) is an (object-discrete) T-monoid. Likewise, if B N TB
 is another T-monoid and M p TN is a horizontal arrow in KMod(Mod(X),T), then
 p(TeB,eA) is a horizontal arrow from M(TeA,eA) to N(TeB,eB). It is straightforward to
 extend these constructions to a functor KMod(Mod(X),T)
 dKMod(Mod(X),T).
 Note that M(Te,e) comes with a natural map to M, whose vertical arrow component
 is e, and likewise for p(TeB,eA). This supplies the counit of the desired coreflection. We
 obtain the unit by observing that if M were already object-discrete, then e would be the
 identity, so we would have M(Te,e) ∼
 =M. The triangle identities are easy to check.
 Note that the horizontal arrow in X underlying M(Te,e) is the restriction of A0
 M (TA)0
 along the identity e0: A0 = A0 and the map (Te)0: T(UA0
 )0
 (TA)0. Since e is b.o. and
 T preserves b.o. morphisms, (Te)0 is an isomorphism; thus the coreflection of M leaves
 its underlying horizontal arrow in X essentially unmodified.
 We now prove (ii); let A and M be as before. We first observe that the T-monoid M
 in Mod(X) has an underlying monoid in Mod(X), namely M(η,1). (This is a special case
 of a general functoriality result we will prove in [CS10a].) As noted in Remark 5.15, a
 monoid in Mod(X) consists of two monoids in X and a monoid homomorphism between
 them whose vertical arrow components are identities. In this case the first monoid is of
 course A. We denote the second by A′ and the monoid homomorphism by c: A
 A′.
 Note that the underlying horizontal arrow of A′ in X is just M(η,1).
46
 Nowsince T preserves b.o. morphisms, TA Tc TA′ is b.o., hence (TA)0 
(Tc)0 (TA′)0
 is an isomorphism. By restricting along its inverse and using the identity (A′)0 = A0,
 from A0
 M (TA)0 we obtain a horizontal arrow (A′)0
 (TA′)0. We abuse notation
 by continuing to denote this M (since restriction along isomorphisms leaves an arrow
 essentially unchanged). Now A′ is a restriction of M, so it acts on M from the left via the
 multiplication of M. And since T preserves restrictions, TA′ is a restriction of TM, so it
 also acts on M from the right via the multiplication of M. Thus, the horizontal arrow in
 X underlying M also admits the structure of a horizontal arrow A′
 TA′ in Mod(X),
 which we denote M′. Likewise, the multiplication and unit of the T-monoid M induce a
 multiplication and unit on M′, making it also into a T-monoid, and we have a canonical
 T-monoid homomorphism M
 M′ which is an isomorphism in X. By definition of A′,
 M′ is normalized. There is an analogous construction on horizontal arrows, and together
 they extend straightforwardly to a functor KMod(Mod(X),T)
 nKMod(Mod(X),T).
 Now recall that A′ came equipped with a b.o. monoid homomorphism A
 A′. It is
 straightforward to check that this homomorphism underlies a T-monoid homomorphism
 M M′; inthis way we obtain the unit of the desired reflection. We obtain its counit
 by observing that if M is already normalized, then A ∼
 = A′ and hence M ∼ = M′. The
 triangle identities are again easy to check.
 Finally, to show (iii), we observe that the unit of the reflection and the counit of
 the coreflection are isomorphisms on the underlying horizontal arrow in X (since they
 are restrictions along an isomorphism). Moreover, the reflection and coreflection functors
 both invert morphisms with this property. Statement (iii) then follows formally.
 Recall that we began this section by observing that ordinary multicategories can be
 recovered as either object-discrete or normalized T-monoids, when T is the “free strict
 monoidal category” monad on Set-Prof. Since this T preserves b.o. morphisms, this
 statement is indeed an instance of Theorem 8.6. However, ordinary multicategories can
 also be obtained as arbitrary S-monoids, when S is the free monoid monad on Set-Mat =
 Span(Set). Noting that in this case T = Mod(S), we generalize this statement to the
 following.
 8.7. Theorem. Let S be a monad on a virtual equipment X. Then the monad Mod(S)
 on Mod(X) preserves b.o. morphisms, and we have a diagram
 dKMod(Mod(X),Mod(S))
 W
 W
 W
 W
 W
 W
 W
 W
 W
 KMod(Mod(X),Mod(S))
 W
 W
 W
 W
 W
 W
 W
 W
 W
 W
 W
 nKMod(Mod(X),Mod(S))
 gggggggggggggggggggg
 KMod(X,S)
 which serially commutes (up to isomorphism). Moreover, the two diagonal functors
 dKMod(Mod(X),Mod(S))
 KMod(X,S)
 nKMod(Mod(X),Mod(S))
 are equivalences.
 KMod(X,S)
 (8.8)
 (8.9)
47
 Proof.Bydefinition, Mod(S) takes a monoid A0
 A A0 toSA0
 SA SA0, soitpreserves
 b.o. morphisms since S preserves isomorphisms. We define the middle vertical arrow
 KMod(Mod(X),Mod(S))
 by applying the 2-functor Mod to the functor
 H-Kl(Mod(X),Mod(S))
 KMod(X,S)
 H-Kl(X,S)
 (8.10)
 which takes a monoid A0
 A A0 to its underlying object A0, and similarly for hori
zontal arrows. (This is again a special case of the general functorial result of [CS10a].)
 Thus, (8.10) takes a Mod(S)-monoid A M Mod(S)(A) to the S-monoid A0
 M SA0.
 We define the diagonal functors by composition with this, so that the triangles
 ?
 ?
 ?
 ?
 and •••• commute by definition. The other triangles commute up to isomorphism because
 the reflection and coreflection were defined to fix A0, replace A, and restrict M along an
 isomorphism, whereas (8.10) simply forgets about A.
 Now, by the 2-out-of-3 property for equivalences, it suffices to show that (8.8) is an
 equivalence. We will construct an explicit inverse to it. By Proposition 5.14, to construct
 a normal functor
 KMod(X,S)
 KMod(Mod(X),Mod(S))
 it suffices to construct a not-necessarily-normal functor
 KMod(X,S)
 H-Kl(Mod(X),Mod(S)).
 (8.11)
 (8.12)
 We define (8.12) on objects by sending an S-monoid A0
 A TA0 to UA0
 , and likewise on
 vertical arrows. A horizontal arrow A p B in KMod(X,S) has an underlying horizontal
 arrow A0
 p TB0 in X, which acquires a T(UB0
 )-module structure from the following
 composite:
 A0
 A0
 A0
 A0
 A0
 A0
 A0
 A0
 p
 =
 p
 TB0
 TB0
 TB0
 TB0
 TB0
 TB0
 TB0
 TB0
 ¯
 pr
 p
 T(UB0) TB0
 TB0
 Tˆ b
 TB
 Tη
 T2B0
 T2B0
 T2B0
 T2B0
 µ
 TB0
 TB0
 This defines (8.12) on horizontal arrows; its action on cells is straightforward. The in
duced normal functor (8.11) takes an S-monoid A0
 A TA0 to itself, regarded as an
 (UA0
 ,T(UA0
 ))-bimodule. Clearly (8.11) followed by the forgetful functor is the iden
tity, while the composite in the other direction is precisely the coreflection functor into
 dKMod(Mod(X),Mod(S)); this completes the proof.
48
 8.13. Examples.Asremarked above, when S isthe“freemonoid” monadonSpan(Set),
 this shows that ordinary multicategories (i.e. S-monoids) can also be identified with
 object-discrete or normalized Mod(S)-monoids. Likewise, virtual double categories are
 S-monoids for the “free category” monad, and thus can also be identified with object
discrete or normalized Mod(S)-monoids.
 8.14. Example. Since topological spaces can be identified with U-monoids in Rel, they
 can also be identified with object-discrete or normalized Mod(U)-monoids in 2-Prof. In the
 terminology of [Tho09], a Mod(U)-monoid is a modular topological space. It is normalized
 precisely when its order is the specialization order, so that it is equivalent to an ordinary
 topological space—i.e. a U-monoid, as required by Theorem 8.7.
 By no means are all interesting monads on Mod(X) of the form Mod(S). However,
 many of them do preserve b.o. morphisms, so that Theorem 8.6 at least applies.
 8.15. Example. The “free symmetric strict monoidal category” monad on Set-Prof =
 Mod(Set-Mat) preserves b.o. morphisms but is not of the form Mod(S) for any monad S
 on Set-Mat. We have seen in Example 4.16 that object-discrete T-monoids are symmetric
 multicategories; hence so are normalized T-monoids.
 8.16. Example. The “free category with strictly associative finite products” monad on
 Set-Prof also preserves b.o. morphisms but is not of the form Mod(S). We have seen in
 Example 4.17 that object-discrete T-monoids are multi-sorted Lawvere theories; hence so
 are normalized T-monoids.
 8.17. Non-Example.RecallfromExample4.19thatclubs areT-monoidsin Span(Cat)
 with a discrete category of objects, where T is a monad like the previous two. However,
 since Span(Cat) is not of the form Mod(X), the theory of this section does not apply to
 clubs. In particular, their “object-discreteness” is not an instance of our definition, and
 is not the same as normalization.
 When T does not preserve b.o. morphisms, however, normalized and discrete T
monoids can be quite different, even on a virtual equipment of the form Mod(X). In
tuitively, saying that T preserves b.o. morphisms says that the possible domains of multi
morphisms in a T-multicategory depend only on its objects. If this fails to be true,
 then how many morphisms are included in the underlying monoid can change what these
 possible domains are.
 8.18. Example.Let T bethe “free category with equalizers” monad on Set-Prof. Then
 T evidently does not preserve b.o. morphisms, but it is the identity on discrete categories.
 Therefore, an object-discrete T-monoid is just a category, whereas a normalized T-monoid
 can have morphisms whose domain is a “formal equalizer” of ordinary morphisms.
 More interestingly, normalized T-monoids for the “free category with finite limits”
 monad (which also does not preserve b.o. morphisms) can be considered a generalization
 of Lawvere theories to finite-limit logics. We can also continue to generalize to more
 powerful logics (or “doctrines”).
49
 These examples suggest that when T does not preserve b.o. morphisms, it is often the
 normalized, rather than the object-discrete, T-monoids that better capture the desired
 notion of T-multicategory. Note also that normalization makes sense for any monad
 on a virtual equipment, while object-discreteness only makes sense for monads on virtual
 equipments of the form Mod(X). Finally, we will see in the next section that normalized T
monoids are the most natural notion to compare with pseudo T-algebras. This inspires us
 to take normalized T-monoids as our preferred definition of “generalized multicategory,”
 and to make the following informal definition.
 8.19. Definition. If T is a monad on a virtual equipment for which (possibly pseudo)
 T-algebras are called widgets, then normalized T-monoids are called virtual widgets.
 The reasons for this definition were summarized in the introduction. In §9 we will prove
 that any widget has an underlying virtual widget, further justifying the terminology. Of
 course, we have seen that a number of types of virtual algebras already have their own
 names, such as “multicategory” and “Lawvere theory.” When such common names exist,
 we of course use them in preference to terms such as “virtual monoidal category” or
 “category with virtual finite products.”
 Note that “virtual widget” is, strictly speaking, ambiguous: knowing the notion of
 widget determines at most the vertical 2-category VX and the 2-monad VT, rather than
 X and T themselves. However, many 2-categories that arise in practice come with an
 obvious “natural” extension to a virtual equipment, so in practice there is little ambiguity.
 (In fact, there is a general construction of an equipment from a well-behaved 2-category;
 see [CJSV94].) One case of ambiguity is if “widget” is the name for T-algebras in Set
 or Cat, but we consider T-monoids in V-Mat or V-Prof; in this case we may speak of
 V-enriched virtual widgets.
 8.20. Remark.The discussion above suggests that when the objects of X are category
like, it is the normalized T-monoids (i.e. virtual T-algebras) that are more important,
 while when the objects of X are set-like, it is the non-normalized T-monoids (i.e. virtual
 Mod(T)-algebras) that are more important. This does seem to usually be the case, but
 there are exceptions on both sides, such as the following.
 • As we have already remarked, the multicategories of [BD98] and [Che04] are non
normalized T-monoids, when T is the “free symmetric strict monoidal category”
 monad on Set-Prof (whose objects are obviously category-like).
 • Let U bethe ultrafilter monad on Rel, whose objects are set-like. We have seen that
 a U-monoid is just a topological space, but it is easy to verify that a U-monoid is
 normalized just when it is a T1-space—certainly also an important concept.
 1. Representability
 We now turn to a general version of the comparison between monoidal categories and
 multicategories. Of course, we first need to identify the analogue of a monoidal category
50
 in the general case. We saw in §8 that ordinary multicategories have two different faces in
 our setup: they are the S-monoids where S is the “free monoid” monad on Span(Set), and
 also the normalized T-monoids, where T = Mod(S) is the “free strict monoidal category”
 monad on Set-Prof. Monoidal categories, however, are more visible from the second point
 of view: they are the pseudo V(T)-algebras in V(Set-Prof) = Cat.
 Accordingly, in this section we will assume that T is a monad on a virtual equipment
 X whose objects are “category-like,” and seek to compare (pseudo) V(T)-algebras with
 (normalized) T-monoids. We will additionally have to assume that T is a normal monad
 as defined in §6, since otherwise it doesn’t even induce a 2-monad on V(X). If we are
 given instead a monad S on a virtual double category whose objects are “set-like,” then
 in order to apply the theory of this section we simply consider Mod(S) instead; some
 examples of this can be found later on. Generalizing the terminology of [Lei04, p. 165],
 we may call a (pseudo) V(Mod(S))-algebra an S-structured monoid.
 Actually, the most natural approach to the comparison turns out to be via oplax T
algebras. Recall that for a 2-monad T on a 2-category, an oplax T-algebra is an object
 A with a map a: TA Aand 2-cells
 T2A µ
 Ta
 a
 TA
 a
 TA a A
 A η
 C
 C
 C
 C
 C
 C
 C
 C
 {{{
 TA
 C
 and
 C
 {{{
 ba
 C
 C
 C
 C
 C
 C
 a
 A
 (9.1)
 satisfying certain straightforward axioms. We call it normal if a is an isomorphism, and a
 pseudo T-algebra if both a and a are isomorphisms. Finally, if T is a monad on a virtual
 equipment, we will always abuse terminology by saying “T-algebra” (with appropriate
 prefixes) to mean V(T)-algebra.
 9.2. Theorem. Let T be a normal monad on a virtual equipment X. Then:
 (i) Any oplax T-algebra TA a A in VX gives rise to a T-monoid A A(a,1) TA, which
 is normalized if and only if A is normal.
 (ii) A T-monoid A M TA arises from an oplax T-algebra if and only if M ∼ = A(a,1)
 for some vertical arrow TA a A.
 Proof. If a: TA
 induces a unit cell
 A is an oplax T-algebra, then by definition of A(a,1), the 2-cell a
 A UA A
 η
 AA(a,1)
 TA.
51
 Likewise, by the dual of Corollary 7.21, a induces a multiplication
 A A(a,1) TA(TA)(Ta,1)T2A
 µ
 A
 A(a,1)
 TA
 and using the isomorphism (TA)(Ta,1) ∼ = T(A(a,1)) (since T is normal) we obtain a
 multiplication cell. The axioms to make A(a,1) into a T-monoid follow directly from the
 axioms for an oplax T-algebra. To complete (i), we observe that a is an isomorphism if
 and only if the induced cell UA
 A(aη,1) ∼ = A(a,1)(η,1) is an isomorphism, which says
 precisely that the unit defined above is cartesian. Conversely, if A M TA is a T-monoid
 and M ∼ = A(a,1), then the same bijections supply 2-cells a and a satisfying the same
 axioms making a: TA
 A into an oplax T-algebra; this shows (ii).
 The following example may serve to clarify the connection between normality of oplax
 T-algebras and normalization of T-monoids.
 9.3. Example. Let T be the “free strict monoidal category” monad on Set-Prof. Then
 an oplax T-algebra is an oplax monoidal category: a category A equipped with tensor
 product functors
 A×···×A A
 (x1, . . ., xn) → x1 ⊗... ⊗ xn
 for n ≥ 0, and transformations
 x
 x11 ⊗... ⊗xnkn
 x
 x11 ⊗... ⊗x1k1
 ⊗...⊗xn1 ⊗...⊗xnkn
 satisfying certain evident axioms. Note that the 0-ary tensor product 
is a “lax unit”
 and the 1-ary tensor product x is not necessarily isomorphic to x, only related by the
 given unit transformation x
 x.
 As mentioned previously, a T-monoid consists of a category A, a multicategory M with
 the same objects, and an identity-on-objects functor from A to the underlying ordinary
 category of M. Now Theorem 9.2 says that we can make an oplax monoidal category
 into a T-algebra by defining the multimorphisms in M from (x1,...,xn) to y to be the
 morphisms x1 ⊗...⊗xn
 y in A.
 Note that the morphisms from x to y in the underlying ordinary category of M are the
 morphisms from x to y in A. The functor A M is defined by composing with the unit
 transformation x
 x. Clearly this is fully faithful (i.e. the T-monoid is normalized)
 just when x
 x is an isomorphism (i.e. the oplax T-algebra is normal).
 The following characterization of pseudo T-algebras is now obvious.
52
 9.4. Corollary. A normalized T-monoid A M TA arises from a pseudo T-algebra
 if and only if
 (i) M ∼ = A(a,1) for some TA a A, and
 (ii) the induced 2-cell a is an isomorphism.
 We say that a normalized T-monoid is weakly representable if it satisfies (i), and
 representable if it satisfies both (i) and (ii) (hence is equivalent to a pseudo T-algebra).
 9.5. Example. When T is the “free strict monoidal category” monad on Set-Prof,
 Corollary 9.4 specializes to the characterization of monoidal categories as representable
 multicategories, as in [Her00] and [Lei04, §3.3]. We will see in §B.14 that it also includes
 the general representability notion of [Her01]. The analogue of Theorem 9.2 in the lan
guage of [Bur71] can be found in [Pen09], which uses “representable” for what we call
 “weakly representable” and “lax algebra” for what we call an “oplax algebra.”
 9.6. Remark. Strictly speaking, the notion of monoidal category obtained in this way
 is the “unbiased” version, which is equipped with a specified n-ary tensor product for all
 n ≥ 0, instead of the usual “biased” version having only a binary and nullary product
 (see [Lei04, §3.1]). This is generally what happens for pseudoalgebras: if T is a monad
 whose strict algebras are some strict structure, then pseudo T-algebras are an “unbiased”
 sort of weak structure. Generally the unbiased version is equivalent to the biased one,
 but there is real mathematical content in this statement; for instance, the equivalence of
 biased and unbiased monoidal categories is essentially equivalent to Mac Lane’s coherence
 theorem.
 9.7. Example. Recall that virtual double categories can be identified with S-monoids
 for the “free category” monad S on directed graphs, and hence also with normalized
 Mod(S)-monoids. In this case it is easy to check that for a normalized Mod(S)-monoid
 A M TA, we have M ∼ = A(a,1) iff every composable string of horizontal arrows is
 the source of a weakly opcartesian arrow (see Remark 5.8). Thus, such virtual double
 categories can be identified with “normal oplax double categories,” which are equipped
 with n-ary composites for all n and comparison maps
 p11 ⊙ ···⊙pnkn
 and invertible comparison maps
 p11 ⊙··· ⊙p1k1
 ⊙···⊙pn1 ⊙···⊙pnkn
 p ∼ = p
 satisfying analogous axioms to an oplax monoidal category. Condition (ii) in Corollary 9.4
 is then equivalent to requiring weakly opcartesian cells to be closed under composition.
 As observed in Remark 5.8, this suffices to ensure we have a pseudo double category, i.e.
 a pseudo Mod(S)-algebra.
53
 9.8. Example.Let U bethe ultrafilter monad on Rel. We have seen that a U-monoid is
 a topological space, and a normalized U-monoid is a T1-space. A vertical U-algebra (which
 is automatically strict, since V(Rel) is locally discrete) is a compact Hausdorff space, and
 in this case Theorem 9.2 tells us what we already knew: any compact Hausdorff space is,
 in particular, a T1 topological space.
 Now consider the induced monad Mod(U) on Mod(Rel). The objects of Mod(Rel) =
 2-Prof are preorders. In the language of [Tho09], a strict Mod(U)-algebra is an ordered
 compact Hausdorff space, whereas by Theorem 8.7 a normalized Mod(U)-monoid is simply
 a topological space. Thus, Theorem 9.2 tells us that any ordered compact Hausdorff space
 X can be equipped with a topology in which an ultrafilter F converges to a point y if and
 only if the (unique) limit of F in X is ≤ y in the given preorder.
 The next three examples can all be found in [Her01] (see B.14 for more on the com
parison between our setting and Hermida’s).
 9.9. Example. Let S be a small category and T the monad on C = Setob(S) whose
 algebras are functors S
 Set, as in Example 4.10, and consider the monad Mod(T)
 on Mod(Span(C)) = Prof(C). A strict Mod(T)-algebra is a functor S
 Cat, while a
 pseudo Mod(T)-algebra is a pseudofunctor S
 Cat. Now by Theorem 8.7, normalized
 Mod(T)-monoids can be identified with T-monoids, which as we saw can be identified with
 functors A
 S. It is then easy to verify that a normalized Mod(T)-monoid satisfies
 9.4(i) iff the corresponding functor A
 S admits all weakly opcartesian liftings, and
 9.4(ii) iff weakly opcartesian arrows are closed under composition. Thus, in this case
 Corollary 9.4 specializes to the classical equivalence between pseudofunctors S
 Cat
 and opfibrations over S.
 9.10. Example. Let T be as in Example 9.9, but now consider T-monoids rather than
 Mod(T)-monoids. A T-monoid is normalized just when for each x ∈ S, the induced span
 A(x,1)
 M A(x,1)is the identity span; i.e. when the fibers of A
 categories. Such a normalized T-monoid satisfies 9.4(i) iff A
 S are discrete
 S admits all weakly
 opcartesian liftings, which in this case are automatically opcartesian by discreteness.
 Thus, Corollary 9.4 also specializes to the equivalence of functors S
 Set and discrete
 opfibrations over S.
 9.11. Example. Let T be the “free strict ω-category” monad on Span(Globset), for
 which we saw in Example 4.11 that T-monoids on 1 are globular multicategories. Pseudo
 T-algebras are an “unbiased” version of the monoidal globular categories of [Bat98]. Thus
 any monoidal globular category has an underlying globular multicategory, and can be
 characterized among the latter by a representability property.
 The requirement that T be normal in Theorem 9.2 cannot be dispensed with.
 9.12. Example. Let P be the extension of the powerset monad to Rel described in
 Example 3.7. Since V(Rel) = Set is locally discrete, oplax P-algebras are just P
algebras in Set, which can be identified with complete meet-semilattices (the structure
 map PA Atakes a subset X ⊆A to its meet X).
54
 Now, we have observed in Example 4.14 that P-monoids can be identified with closure
 spaces. If we attempt to follow the prescription of Theorem 9.2, starting from a complete
 join-semilattice we would define the “closure operation” c(X) = { X}; but this is neither
 extensive nor monotone.
 On the other hand, if we first apply Mod, we obtain a monad Mod(P) on Mod(Rel) =
 2-Prof, which is normal. By Theorem 8.7, normalized Mod(P)-monoids can be identified
 with P-monoids, i.e. closure spaces. With a little effort, pseudo Mod(P)-algebras can
 be identified with meet-complete preorders (that is, preorders that are complete as cate
gories). Theorem 9.2 then tells us that from a meet-complete preorder we can construct
 a closure space with c(X) = {x | X ≤ x}, which is certainly true.
 We can also make the correspondence of Theorem 9.2 functorial. Recall that for
 any T we have a 2-category KMon(X,T) of T-monoids, defined to be the vertical 2
category of KMod(X,T). It turns out that while T-monoids correspond to oplax T
algebras, morphisms of T-monoids correspond to lax T-algebra morphisms. Recall that a
 lax T-morphism between oplax T-algebras consists of a map f : A
 B and a 2-cell
 TA Tf
 a
 f
 TB
 b
 A f
 B
 satisfying certain straightforward axioms. And if A f
 g
 B are two such, a T-transformation
 is a 2-cell f α g such that
 TA Tf
 a
 A
 f
 f
 g
 α B
 Tf
 TB
 b
 TA
 =
 a
 Tα TB
 Tg
 f
 b
 A f
 B.
 We write Oplax-T-Algl for the resulting 2-category.
 9.13. Theorem. Let T be a normal monad on a virtual equipment X. Then there
 is a strict 2-functor Oplax-T-Algl
 KMon(X,T), whose underlying 1-functor is fully
 faithful, and which becomes 2-fully-faithful (that is, an isomorphism on hom-categories)
 when restricted to normal oplax T-algebras.
 Proof. For oplax T-algebras (A,a) and (B,b), regarded as T-monoids A A(a,1) TA and
 B B(b,1) TB, a morphism of T-monoids consists of a vertical arrow f: A
 B and a
55
 2-cell
 AA(a,1)
 f
 TA
 Tf
 BB(b,1)
 TB
 satisfying certain axioms. But by definition of B(b,1), and by Theorem 7.20 applied to
 A(a,1), this 2-cell is equivalent to one
 TA UTA
 a
 A
 f
 TA
 Tf
 TB
 b
 UB
 .
 This defines a 2-cell b◦Tf
 f ◦a in V(X), which is precisely the additional data required
 to make f into a lax T-algebra morphism. It is easy to verify that the axioms of a T
monoid morphism are equivalent to the axioms of a lax T-algebra morphism under this
 translation, and that composition is preserved.
 Now let f,g: A
 transformation β: f
 B be two such morphisms, and recall from §6 that a T-monoid
 g consists of a cell
 •••••••A
 A
 g
 •
 ⇓β
 ?
 ?
 ?
 ?
 ?
 ?
 ?
 ηTB◦f
 ?
 B
 B
 B
 |
 B(b,1)
 TB
 TB
 TB
 satisfying a certain axiom. Equivalently, β is a 2-cell bηf
 T-algebra transformation α: f
 g in V(X). Thus, given a
 g, it is natural to define β to be the composite
 bηf b bf f α g,
 where b: bη
 1 is the oplax unit map of B. With this definition, the axiom that must be
 satisfied for β to be a T-monoid transformation becomes the following equality of pasting
56
 diagramsinVX.
 B TB b
 A
 B
 f
 A TA a TA
 TB
 Tf f
 ?? ??
 TB T2B Tb
 B
 TB
 η
 B TB b
 TB
 T2B
 η =
 B
 B • • • • • • • • • •
 • • • • • • • • • •
 A
 B
 g
 OO OO
 α
 b b
 ?? ??
 B TB b
 b
 ?? ??
 B TB b
 B
 B
 B T2B T2B
 TB
 µB
 =
 B TB b
 A
 B
 g
 A TA a TA
 TB
 Tg g
 ?? ??
 TA
 TB
 Tf
 TB
 T2B
 TηB
 TB
 TB • • • • • • • • • •
 • • • • • • • • • •
 Tα
 Tb b
 ?? ??
 TB T2B Tb
 b
 ?? ??
 B TB. b
 B
 B
 B T2B T2B
 TB.
 µB
 (9.14)
 Thecellmarked“=”isanidentitybyProposition7.25appliedtoacellcomponentofη.
 Now, twooftheaxiomsforanoplaxT-algebrasaythat
 TB T2B Tb
 B
 TB
 η
 B TB b TB
 T2B
 η =
 B
 B • • • • • • • • • •
 • • • • • • • • • • b b
 ?? ??
 B TB b
 b
 ?? ??
 B TB b
 B
 B
 B T2B T2B
 TB
 µB
 = B TB
 b
 b
 1B
 =
 TB
 T2B
 TηB
 TB
 TB • • • • • • • • • •
 • • • • • • • • • • Tb b
 ?? ??
 TB T2B Tb
 B TB b
 b
 ?? ??
 B TB. b
 B
 B
 B T2B T2B
 TB.
 µB
 Afterremovingthesecompositesfrom(9.14),what isleft issimplytheequationforαto
 beaT-algebratransformation; thusαis suchpreciselywhenβ=α.bf isaT-monoid
 transformation.And,ofcourse, ifBisnormal, thenbf isanisomorphism,andsoαcan
 berecovereduniquelyfromβ.We leave it tothereader toverifythat thisassociation
 preservesbothtypesof2-cellcomposition.
 TherestrictiontonormaloplaxalgebrasinthefinalstatementofTheorem9.13cannot
 bedispensedwitheither.
 9.15. Example.LetAandBbeoplaxmonoidal categories, regardedasT-monoids
 forthe“freestrictmonoidalcategory”monadTasinExample9.3,andletA f
 g
 Bbe
 laxmonoidal functors. AT-algebratransformationf g is, inparticular, anatural
 transformationf g,andthereforehascomponentsfx αx gx.However, ifweunravel
 thedefinitionofaT-monoidtransformation,weseethat itscomponentsareof theform
 fx βx gx.Thus,whenBisnotnormal, therecanbenobijectioningeneral.
57
 9.16. Remark. Recall from §1 that generalized multicategories can be regarded as
 “algebraic theories.” For instance, ordinary multicategories correspond to strongly regular
 f
 initary theories, while Lawvere theories correspond to arbitrary finitary theories. In
 language introduced by Jon Beck, one may say that the monad T provides the “doctrine”
 in which the theories are written. (Motivated by this, some authors use the word doctrine
 to mean simply a 2-monad.) If X is a T-monoid, regarded as a theory in the doctrine
 T, and A is a pseudo T-algebra, then it is natural to define a model of X in A to be a
 T-monoid homomorphism from X to (the underlying T-monoid of) A.
 Now, frequently the functor of Theorem 9.13 has a left adjoint FT when restricted
 to pseudo T-algebras and morphisms. In such a case, a model of X in A can equally
 be defined as a T-algebra morphism FTX
 A. That is, FTX is the “free T-algebra
 containing a model of X.” Following [Law63], this is sometimes called the “functorial
 semantics” of T.
 For example, when X is a Lawvere theory, FTX is the category with finite products
 that incarnates it. (In fact, as we remarked in Example 4.17, Lawvere theories are often
 defined to be certain categories with finite products.) Likewise, when X is a Lawvere V
theory, then FTX is the V-category with finite cotensors that incarnates it (see [Pow99])
 and when X is an ordinary or non-symmetric operad, FTX is the “PROP” or “PRO”
 associated to it (see [BV73]).
 This adjunction can also be used to characterize representability. It turns out that the
 strict (resp. pseudo) algebras for the induced 2-monad T⊣ on KMon(X,T) can be identified
 with strict (resp. pseudo) T-algebras. Moreover, T⊣ is a “lax-idempotent” 2-monad in the
 sense of [KL97], so that A is a pseudo T⊣-algebra precisely when the unit A
 T⊣A has a
 left adjoint. Thus the “structure” imposed by the 2-monad T has been transformed into
 “property-like structure” imposed by T⊣. In particular cases, these observations can be
 found in [Her00, Her01, Pen09]; in [CS10b] we will study them in our general context.
 A. Composites in Mod and H-Kl
 In this appendix we consider the question of when Mod(X) and H-Kl(X,T) have compos
ites and units, which will be needed for our comparisons with existing theories in the next
 appendix. The first case is easy; the following was also observed in [Shu08].
 A.1. Theorem.If X is an equipment in which each category HX(A,B) has coequalizers,
 which are preserved on both sides by ⊙, then Mod(X) is also an equipment.
 Proof (Sketch). We have seen already that Mod(X) always has units, and inherits
 restrictions from X, so it remains only to construct composites. We define the composite
 of bimodules A p B q C to be the coequalizer of the two actions of B:
 p ⊙B⊙q p⊙q p⊙Bq
58
 and similarly for longer composites. Given a cell
 p
 f
 q
 r
 g
 in Mod(X), to factor it through p ⊙B q, we first factor it through a cartesian cell to
 obtain a cell (p,q)
 r(g, f) in HX(A,C), then factor this through the coequalizer in
 HX(A,C), and finally compose again with the cartesian cell. Thus (p,q)
 p ⊙B q is
 weakly opcartesian; to show that these cells compose we use the fact that ⊙ preserves
 coequalizers.
 Note that we require X to have restrictions, as well as composites, in order to show
 that Mod(X) has composites. We could instead assume explicitly that the coequalizers in
 HX(A,B) satisfy a universal property relative to all cells, but in practice this generally
 tends to hold only because of the existence of restrictions.
 A.2. Example. If V has small colimits preserved by ⊗, then V-Mat satisfies the hy
potheses of Theorem A.1, so (as we have seen) V-Prof is an equipment.
 A.3. Example.IfChaspullbacks andcoequalizers preserved by pullback, then Span(C)
 satisfies the hypotheses of Theorem A.1, so (as we have also seen) Prof(C) is an equipment.
 We have also already seen that H-Kl(X,T) always inherits restrictions from X. How
ever, to show that it has composites, we require fairly strong conditions not just on X
 but on T as well. Recall that a functor between pseudo double categories (and, therefore,
 also between equipments) is called strong if it preserves all composites. We then make
 the following definition:
 A.4. Definition. A transformation F α G of functors X F
 G
 Ybetween equipments
 is horizontally strong if for every horizontal arrow X p Y in X, the cell induced by
 αp under the bijection of Corollary 7.21:
 FX Fp FYGY(1,αY)GY
 FXGX(1,αX)
 GX Gp
 GY
 is an isomorphism. A monad T on an equipment X is horizontally strong if T is a
 strong functor and µ and η are horizontally strong.
 A.5. Remark.Recall from Remark 7.26 that any transformation α of functors between
 equipments induces an oplax transformation H(α) of functors between horizontal bicat
egories. Horizontal strength of α is equivalent to requiring H(α) to be a strong (aka
 pseudo) transformation (hence the name).
59
 F
 A.6. Example. Let C
 G
 α D beatransformation between pullback-preserving func
tors between categories with pullbacks. It is not hard to verify that the induced trans
formation Span(α) is horizontally strong if and only if α is a cartesian natural trans
formation, meaning that all its naturality squares are pullbacks. Therefore, if T is a
 pullback-preserving monad on C, the monad Span(T) is horizontally strong if and only
 if µ and η are cartesian natural transformations. Such a T is often called a cartesian
 monad; see §B.1.
 A.7. Example. We have remarked that most of the monads from Example 3.7 are not
 even strong functors in general, with the exception of the ultrafilter monad on Rel. One
 can verify that for this monad, the multiplication transformation is horizontally strong,
 but the unit transformation is not; hence it is not a horizontally strong monad.
 A.8. Theorem.IfT is ahorizontally strong monad on an equipment X, then H-Kl(X,T)
 is also an equipment.
 Proof (Sketch). It suffices to show that H-Kl(X,T) has composites. A composable
 string of horizontal arrows
 X0
 p1 X1
 p2 ··· pn Xn
 in H-Kl(X,T) consists of horizontal arrows Xi
 pi+1 TXi+1 in X. Since X is an equipment,
 we can form the composite
 p1 ⊙T(p2)⊙···⊙Tn−1(pn)⊙TXn(1,µn−1)
 in X, which clearly supplies a weakly opcartesian cell in H-Kl(X,T). Likewise, TX(1,η) is
 a weak unit for X in H-Kl(X,T). The assumptions on T are required to show that these
 weakly opcartesian cells compose, or equivalently that this composition is associative;
 rather than write this out in detail we merely compute the 3-fold associativity isomorphism
 for X p Y q Z r W.
 (p ⊙Tq⊙TZ(1,µ))⊙Tr⊙TW(1,µ)
 ∼
 =p⊙Tq⊙T2r⊙T2W(1,µT)⊙TW(1,µ) (strength of µ)
 ∼
 =p⊙Tq⊙T2r⊙T2W(1,Tµ)⊙TW(1,µ) (associativity of µ)
 ∼
 =p⊙Tq⊙T2r⊙T(TW(1,µ))⊙TW(1,µ) (normality of T)
 ∼
 =p⊙T(q⊙Tr⊙TW(1,µ))⊙TW(1,µ)
 Of course, in the unit isomorphisms η is used instead of µ.
 (strength of T).
 A.9. Corollary. If T is a horizontally strong monad on an equipment X, such that
 each category HX(A,B) has coequalizers that are preserved by ⊙ on both sides and also
 preserved by T, then KMod(X,T) is also an equipment.
 Proof. The hypotheses ensure that H-Kl(X,T) satisfies the conditions of Theorem A.1.
60
 A.10. Example.IfT isacartesian monad on acategory C with pullbacks, then we have
 seen that the induced monad on Span(C) is horizontally strong; thus H-Kl(Span(C),T)
 is an equipment. If furthermore C has coequalizers that are preserved by pullback and
 by T, then Corollary A.9 implies that KMod(Span(C),T) is also an equipment.
 For example, the “free M-set” monad (M × −) on Set preserves coequalizers, so we
 have an equipment of M-graded categories. However, the “free monoid” monad does not
 preserve coequalizers, and the virtual equipment of ordinary multicategories is not an
 equipment.
 A.11. Example. Let V be a symmetric monoidal category with small coproducts pre
served by ⊗onbothsides, and let T be the extension of the “free monoid” monad on Set to
 a monad on V-Mat defined in Example 3.12. We have already remarked in Examples 5.11
 that T is strong, and an easy calculation shows that it is in fact horizontally strong. Thus,
 H-Kl(V-Mat,T) is an equipment. However, even if V is cocomplete, and in particular
 has coequalizers preserved by ⊗ on both sides, these coequalizers will not in general be
 preserved by T. Thus, the virtual equipment KMod(V-Mat,T) of V-enriched ordinary
 multicategories fails to be an equipment. (For V = Set we have seen this already in the
 previous example.)
 A.12. Example. Let V be a cocomplete symmetric monoidal category with small col
imits preserved by ⊗ on both sides, and let T be the “free symmetric strict monoidal V
category” monad on V-Prof from Examples 3.14 and 4.16. We remarked in Examples 5.12
 that T is strong. In fact, it is easily seen to be horizontally strong, so that H-Kl(V-Prof,T)
 is an equipment. As in the previous example, however, T fails to preserve coequalizers in
 H(V-Prof)(A,B), so that KMod(V-Prof,T) is not an equipment even when V = Set.
 When the horizontal arrows in H-Kl(Set-Prof,T) are identified with the generalized
 structure types of [FGHW08] as in Remark 4.20, their horizontal composites are iden
tified with the substitution operation on structure types. In [FGHW08] the bicategory
 H(H-Kl(Set-Prof,T)) was constructed in this way from structure types and substitution.
 A.13. Example. Let T be the “free category with strictly associative finite products”
 monad on V-Prof from Examples 3.15 and 4.17. We remarked in Examples 5.12 that T
 is strong if V is cartesian monoidal. In fact, in this case it can moreover be shown to be
 horizontally strong, so that H-Kl(V-Prof,T) is an equipment.
 Nowwespecialize to V = Set. If 1 denotes the terminal category, then T1 is equivalent
 to Setop
 f , the opposite of the category of finite sets. Thus, a profunctor 1
 equivalent to a functor Setf
 T1 is
 Set, which (since Set is locally finitely presentable)
 is equivalent to a finitary endofunctor of Set. It is then not hard to verify that the
 equivalence
 H(H-Kl(Set-Prof,T))(1,1) ≃ [Setf,Set]
 is actually an equivalence of monoidal categories, and thus induces an equivalence between
 categories of monoids. But a monoid in H(H-Kl(Set-Prof,T))(1,1) is a T-monoid 1
 T1,
 i.e. a Lawvere theory; thus we recover the classical result of [Law63] that Lawvere theories
 can be identified with finitary monads on Set.
61
 An analogous argument for the “free V-category with finite cotensors” monad on
 V-Prof from Examples 3.16 and 4.18 reproduces the result of [Pow99] that Lawvere V
theories can be identified with finitary V-monads on V. In this case, H-Kl(V-Prof,T)
 seemingly need not be an equipment, but at least the multicategory H-Kl(V-Prof,T)(1,1)
 is a monoidal category, precisely because it can be identified with the monoidal category
 of finitary endofunctors of V under composition.
 A.14. Example. Let Set-Profls denote the virtual double category whose objects are
 locally small categories (that is, large categories with small hom-sets), whose vertical
 arrows are functors, and whose horizontal arrows are profunctors taking values in small
 sets. Then there is a monad T on Set-Profls whose algebras are categories with all small
 products, and we have T1 ≃ Setop. Thus, by analogous reasoning to Example A.13,
 we see that T-monoids 1
 T1 for this T can be identified with arbitrary monads on
 Set. We can likewise obtain monads on any suitable V by using the monad for arbitrary
 cotensors on V-Profls. In [CS10a] we will see that by regarding monads as particular
 generalized multicategories in this way, we can recover the monad associated to an operad
 (as originally defined in [May72]) as a particular case of the functoriality of generalized
 multicategories.
 B. Comparisons to previous theories
 We now describe the existing approaches to generalized multicategories, and show how
 they compare to our theory. Most existing approaches turn out to be instances of our
 theory, applied to a particular sort of monad on a particular sort of virtual equipment.
 Unsurprisingly, however, often more can be said in such special cases that is not true in
 general. Thus, in each section below we briefly mention some of the additional results
 that different authors have obtained in their particular contexts.
 B.1. Cartesian Monads. In order to study and define a type of n-category, Leinster
 developed a theory of cartesian monads and their associated multicategories. This theory
 was developed in a series of papers, eventually culminating in his book [Lei04]. Recall the
 following from Example A.6:
 B.2. Definition. Let E be a category with pullbacks. A monad (T,η,µ) on E is carte
sian if T preserves pullbacks, and all naturality squares of η and µ are pullbacks.
 Given a cartesian monad, Leinster constructs a bicategory E(T) of T-spans and defines
 a (E,T)-multicategory (or simply a T-multicategory) to be a monad in E(T). To compare
 this to our context, recall that whenever E has pullbacks, Span(E) is an equipment, and
 any pullback-preserving monad T on such a E extends to a strong monad on Span(E),
 which is horizontally strong just when T is cartesian. It is then easy to see:
 B.3. Proposition. For a cartesian monad T on E, Leinster’s bicategory E(T) is iso
morphic to H(H-Kl(Span(E),T)).
62
 Therefore, Leinster’s category of (E,T)-multicategories is the vertical category of our
 KMod(Span(E),T). In particular, what he calls a T-operad is a T-monoid 1
 T1 in
 Span(E).
 Actually, Leinster constructs the whole virtual double category KMod(Span(E),T)
 (which he calls an fc-multicategory) in [Lei04, §5.3], and uses it to define transformations
 of his generalized multicategories just as we did in §6. (The notes at the end of his §5.3
 also point in the direction of our §§5 and 7.)
 Leinster also proves most of the results of our §9 in his context, as well as the func
toriality of the construction mentioned in Remark 4.4. Furthermore, he shows that if T
 is a “suitable” cartesian monad on a “suitable” cartesian category E, then the category
 of (E,T)-multicategories is itself monadic over a cartesian category of “T-graphs,” and
 this monad is also cartesian. Thus the process can be iterated, leading to a definition of
 the “opetopes” used in the Baez-Dolan definition of weak n-categories. Finally, Leinster
 also studies algebras for generalized operads, which are closely related to the horizontal
 arrows in KMod(X,T).
 B.4. Clubs. Essentially the same theory was developed in [Kel92] for the case of gen
eralized operads (generalized multicategories on 1). Observe that when T is a cartesian
 monad on a category E with finite limits, so that H-Kl(Span(E),T) is an equipment, then
 in particular the category
 E/T1 ≃H(H-Kl(Span(E),T))(1,1)
 inherits a monoidal structure. It is easy to verify that this monoidal structure on E/T1 is
 the same as that constructed by Kelly (see the explicit description in [Kel92, p. 174–175]).
 Kelly defined a club over T to be a monoid for this monoidal structure; thus such clubs
 can be identified with T-monoids 1
 T1 in Span(E). He also proved that such clubs
 are essentially equivalent to cartesian monads equipped with a “cartesian map” to T.
 (Actually, in [Kel92] it was assumed that T preserves certain pullbacks rather than
 all pullbacks. This suffices to construct a monoidal structure on E/T1, though not for T
 to define a monad on all of Span(E).)
 B.5. Pseudomonads on Prof. The existing theory which is probably closest to our
 approach involves the construction of a Kleisli bicategory from a pseudomonad on a bicat
egory such as V-Prof. A general theory of multicategories based on such pseudomonads
 does not appear to exist in the literature, but it is implicit in [BD98, Che04, FGHW08,
 Gar08, DS03] among other places.
 The general framework is, however, quite simple to state: from a pseudomonad T on a
 bicategory B, one can construct the Kleisli bicategory BT and consider monads in BT as a
 notion of generalized multicategory. (Leinster’s approach is a special case of this for B =
 Span(C), as is Hermida’s for a different bicategory—see §B.14, below.) The relationship
 with our theory is that if T is a horizontally strong monad on an equipment X, it gives
 rise to a pseudomonad H(T) on the bicategory H(X), and H(X)H(T) ≃ H(H-Kl(X,T)) so
 that the resulting notions of multicategory agree.
63
 In the converse direction, of course not every pseudomonad on H(X) arises from a
 monad on X itself, but we have seen that this is true for most monads relative to which
 one may want to define generalized multicategories. In a few cases, however, the extension
 to X may not be vertically strict, necessitating the extension of vEquip to a tricategory.
 Note that if T is also co-horizontally strong, in the sense that its horizontal dual is
 horizontally strong, then it also induces a pseudo-comonad ˆ
 H(T) on the bicategory H(X).
 From this perspective, T-monoids can be identified with lax ˆ
 H(T)-coalgebras. Of course,
 if we work in the horizontal dual, then ˆ
 H(T) becomes a pseudomonad and T-monoids are
 its lax algebras. This is the terminology used by several authors, including Hermida. The
 authors of [DS03] consider the special case when the bicategory B is monoidal and T is its
 free monoid monad, so that T-monoids can be called lax monoids. Such lax monoids can
 also be described directly in terms of B, without the need for cocompleteness hypotheses
 to ensure that T exists.
 B.6. (T,V)-algebras.Following Barr [Bar70], [CT03] started a series of papers which
 described the ideas of a “set-monad with lax extension to V-Mat”, as well as the (T,V)
algebras associated to these monads. Barr’s original idea showed that the “lax algebras”
 of the ultrafilter monad are topological spaces; Clementino and Tholen’s idea extended
 this further, developing a framework that eventually included not only topological spaces,
 but also metric spaces, approach spaces, and closure spaces.
 In the work on (T,V)-algebras, two definitions of set-monad with lax extension to
 V-Mat have been proposed. The original version was applicable to all monoidal V.
 However, it failed to capture all relevant examples, and so a second, slightly different defi
nition was proposed in [Sea05], which captured further examples. However, this definition
 was only applicable when V was a preorder. As we shall see, Seal’s definition turns out
 to be equivalent to asking for a monad on V-Mat (in the case when V is ordered), while
 the original definition is equivalent to asking for a monad on V-Mat which is normal.
 The original definition, given in [CT03], was as follows:
 B.7. Definition. A set monad with lax extension to V consists of a monad
 (T,η,µ) on Set, together with a lax functor TM on V-Mat such that:
 • TM is the same as T on objects and functions (viewed as V-matrices),
 • the comparisons (TMs)(TMr)
 TM(sr) are isomorphisms when r is a function,
 • when viewed as transformations on TM, η and µ have op-lax structure.
 In general, however, this definition was found to be too restrictive, as it didn’t allow
 for examples such as extensions of the powerset monad, whose algebras would be closure
 spaces. To include this type of example, the requirement that TM was the same as T on
 functions needed to be removed. Seal’s definition, given in [Sea05], was the following:
 B.8. Definition. Suppose that V is a monoidal preorder. A set monad with lax
 extension to V consists of a monad (T,η,µ) on Set, together with a lax functor TM on
 V-Mat which is the same as T on objects, and satisfies
64
 (i) Tf ≤ TMf,
 (ii) (Tf)◦ ≤ TMf◦.
 Here, ()◦ denotes taking the opposite V-matrix. By [Sea05, p. 225] the conditions
 imply that if q is a V-matrix and f a function, then TM(qf) = (TMq)(Tf) and TM(f◦q) =
 (Tf)◦(TMq).
 In [Sea05, p. 203], he also shows that when V is completely distributive, η and µ have
 op-lax structure. However, this is not a priori required in his definition. If, however, we
 include this axiom in his definition, then his notion of set monad with lax extension is
 equivalent to giving our notion of a monad on the virtual double category V-Mat.
 B.9. Proposition. Suppose that V is a monoidal preorder. If T is a set monad with
 lax extension TM (in the sense of Seal) for which η and µ are op-lax, then we can define
 a monad T on V-Mat which is T on vertical arrows, and TM on horizontal arrows.
 Conversely, given a monad T on V-Mat, we can define a set monad with lax extension
 which is T on functions, and uses the horizontal action of T to define TM.
 Proof. Suppose that we have a set monad with lax extension to V, in the second sense
 given above. Define a functor T on the double category V-Mat, which is T on vertical
 arrows, and TM on horizontal arrows. Using the η and µ, we get all of the necessary data
 for a monad on V-Mat, with the exception of checking that
 X
 X
 W 
f
 X
 W
 W
 p
 q
 Y
 YY
 g
 Z
 Z
 Z
 implies
 TX
 TX
 TX
 Tf
 TW
 Tp
 TY
 TY
 TY
 Tg
 TW TZ
 TW TZ
 Tq
 TZ
 This is equivalent to checking that p ≤ g◦qf ⇒ TM(p) ≤ (Tg)◦TMq(Tf). But this is easy
 to check by using the two results given after Seal’s definition.
 TM(p) ≤ TM(g◦qf) = (Tg)◦TM(qf) = (Tg)◦(TMq)(Tf)
 Conversely, suppose that we have a monad T on V-Mat. We would like to define a
 lax extension of T (considered as a Set-monad) to V-Mat. Define TM on matrices as for
 T. The only conditions we need to check are Tf ≤ TMf and (Tf)◦ ≤ TMf◦. To show the
 f
 irst is equivalent to showing that TB(1,Tf) ≤ T(B(1,f)). To show this, recall that we
 have a cartesian cell
 A
 A
 f
 B
 B
 B(1,f)
 B
 B
 B
 B
 UB
65
 Moreover, sinceT isafunctor, itpreservescartesiancells(Theorem7.24),andso
 TA TB T(B(1,f))
 TB TB T(UB)
 TA
 TB
 Tf
 TB
 TB
 isalsocartesian.Wecanthusfactorthecell
 TA TB TB(1,Tf)
 TB TB UTB
 TA
 TB
 Tf
 TB
 TB TB
 TB
 TB
 TB TB TB T(UB)
 throughittogetacell
 TA TB TB(1,Tf)
 TA TB T(B(1,f))
 TA
 TA
 TB
 TB
 asrequired.Thesecondinequalityfollowssimilarly,usingthecartesiancell
 B A B(f,1)
 B B UB
 A
 B
 f
 B
 B
 Thus,amonadonV-Matdefinesaset-monadwithlaxextensiontoV-Mat.
 ForgeneralV,wecanalsousetheabovecorrespondencetorecoverthefirstnotionof
 notionofset-monadwithlaxextension: theyarethemonadswhicharenormal.
 B.10. Proposition.Usingtheabovecorrespondence,wegetaset-monadwithlaxex
tensioninthefirstsenseifandonlyif themonadTonV-Mat isnormal.
 Proof.Supposewehaveaset-monadTwithlaxextensionTMinthefirstsense. Then
 wehaveTMf∼ =Tf forall functionsf, andwegetamonadonV-Mat. Moreover,we
 alsohaveT(B(1,f))∼ =TB(1,Tf). Inparticular,wehaveT(A(1,1))∼ =TA(1,1). But
 A(1,1)∼ =UA, sowehaveT(UA)∼ =UTA.ThusT isnormal.
66
 Conversely, suppose that we have a monad T on V-Mat which is normal. We would like
 to show that T(B(1,f)) ∼ = TB(1,Tf). Using the factoring as for the above proposition,
 we get a cell in one direction. To get the other direction, we factor
 TA
 TA
 TA
 Tf
 TB
 TB
 TB
 TB
 TB
 TB
 TB
 TB
 T(B(1,f))
 T(UB)
 UTB
 TB
 TB
 TB
 TB
 TB
 TB
 TB
 TB
 TB
 TB
 TB
 TB(1,Tf)
 TA
 TA
 TA
 through
 Tf
 TB
 TB
 TB
 UTB
 TB
 TB
 TB
 TB
 TB
 TB
 (note that the bottom cell on the left exists by normality of T). The composites of the
 two cells are identities by the universal property of the cartesian cells, and so we have
 T(B(1,f)) ∼ = TB(1,Tf), as required. We also need to check the condition that the
 comparison cell be an isomorphism when r is a function. However, this is equivalent to
 asking that T(r(1,s)) ∼
 =Tr(1,Ts), and this follows from Theorem 7.24.
 For a set-monad with lax extension T, the category of (T,V)-algebras that Tholen,
 Clementino and Seal define is exactly the vertical category of the virtual double category
 KMod(V-Mat,T). They also describe (T,V)-modules, and these are the horizontal arrows
 of KMod(V-Mat,T).
 In addition to providing a more conceptual explanation of the notion of lax extension,
 and a way to compare (T,V)-algebras with other notions of generalized multicategory, our
 general framework improves the theory of (T,V)-algebras in two ways. Firstly, it gives a
 context in which the horizontal Kleisli construction makes sense; such a construction has
 been recognized as desirable (see, for example, [Tho07, p. 7]), but is impossible using only
 bicategories since the monads used in this case are not horizontally strong. Secondly, it
 provides a general reason for the observation of [Tho07, p. 15] that any set-monad with
 lax extension to V-Mat can also be extended to a monad on V-Cat with a lax extension
 to V-Prof (we simply apply the 2-functor Mod).
 There are, however, other special aspects of the theory of (T,V)-algebras which we
 have not discussed. One is that the category of (T,V)-algebras is generally topological
 over Set, and has many other similar formal properties. Another is the use of the “pro”
 construction found in [CHT04]. This is useful to describe additional topological structures;
 for example, monoids in pro-Rel are quasi-uniform spaces. In general, given a virtual
 double category X, one can define a new virtual double category pro-X, and go on to
 describe “pro-generalized multicategories”. Further discussion of this, however, awaits a
 future paper.
 B.11. Non-cartesian monads. The earliest work on generalized multicategories was
 by Burroni in [Bur71]. His framework is very similar to Leinster’s (see §B.1) except
 that he requires nothing at all about the monad T, not even that it preserve pullbacks
 (although the category E must still have pullbacks). This level of generality does not
67
 f
 it into our existing framework, since if T does not preserve pullbacks then it does not
 induce a functor on Span(E) of the sort we have defined. However, it does induce an oplax
 functor between pseudo double categories.
 The simplest way for us to define an oplax functor is to say it is a functor between
 pseudo double categories regarded as co-virtual double categories. Pseudo double cat
egories, oplax functors, and transformations form a 2-category, and we define an oplax
 monad on a pseudo double category to be a monad in this 2-category. Since any functor
 on a category E with pullbacks induces an oplax functor on Span(E), any monad on such
 an E induces an oplax monad on Span(E). Moreover, we can extend our framework to
 deal with oplax functors as follows.
 B.12. Definition. If T is an oplax monad on a pseudo double category X, the hori
zontal Kleisli virtual double category H-Kl(X,T) of T is defined as follows.
 • Its objects, vertical and horizontal arrows, and cells with nullary source are defined
 as when T is a lax functor.
 • A cell
 X0
 X0
 X0
 f
 Y0
 Y0
 Y0
 in H-Kl(X,T) is a cell
 X0
 f
 Y0
 in X.
 p1
 X1
 X1
 p2
 X2
 X2
 α
 q
 p3
 p1⊙T(p2⊙T(···T(pn−1⊙Tpn)···))
 q
 · · ·
 · · ·
 pn
 TnXn
 Xn
 Xn
 Xn
 g
 Y1
 Y1
 Y1
 Tg◦µn
 TY1
 • Composition is defined using the multiplication, unit, and oplax structure of T. For
 example, the composite of
 ⇓α
 is given by the composite
 ⇓β
 ⇓δ
 ⇓γ
 δ ◦(α⊙T(β ⊙Tγ))◦(1⊙µ)◦(1⊙T(1⊙µ))◦T⊙
 in X,where T⊙ is a composite of the oplax structure maps of T:
 p1 ⊙T(p2⊙T(p3⊙T(p4⊙T(p5⊙Tp6))))
 p1 ⊙Tp2⊙T2(p3⊙Tp4⊙T2(p5⊙Tp6))
 Note that when T is a strong functor, both definitions of H-Kl(X,T) make sense;
 however, in this case, they are equivalent.
68
 B.13. Definition. If T is an oplax monad on a pseudo double category X, then a
 T-monoid is a monoid in H-Kl(X,T), and we write KMod(X,T) = Mod(H-Kl(X,T)).
 To compare this to Burroni’s definition, note that H-Kl(X,T) clearly has weak com
posites, and hence is an oplax double category (see Example 9.7). Burroni works instead
 with what he calls a pseudo-category, and what we would probably call a lax-biased bi
category: a bicategory-like structure with units and binary composites and noninvertible
 comparison maps
 p
 p
 p ⊙UA
 UB ⊙p
 p ⊙(q ⊙r) (p⊙q)⊙r.
 satisfying suitable axioms. In fact, of course, Burroni’s “pseudo-category of T-spans”
 extends to a lax-biased double category. Moreover, any lax-biased double category defines
 an oplax double category (and hence a virtual double category), if we take the n-ary
 composite to be
 p1 ⊙···⊙pn = p1⊙(p2⊙···(pn−1 ⊙pn)···).
 (Burroni points this out as well; see [Bur71, p. 66, example 3]. He refers to virtual double
 categories as simply “multicat´egories”.) In this way, Burroni’s Sp(T) is identified with our
 H(H-Kl(Span(E),T)), and thus his “T-categories” can be identified with our T-monoids.
 However, he must move outside the bicategory (or “pseudo-category”) framework to define
 functors of T-categories, whereas they emerge naturally from our setup.
 Burroni also constructs the left adjoint FT from Remark 9.16, and proves the func
toriality of his construction under lax morphisms of monads. Working with his lan
guage, [Pen09] gives a version of the representability results from §9.
 B.14. Cartesian 2-monads. We have described the horizontal arrows A
 Set-Prof as profunctors, i.e. functors Bop × A
 B in
 Set, but it is well-known that such
 functors can equivalently be described by two-sided discrete fibrations, and that this notion
 can be internalized to a sufficiently well-behaved 2-category. [Her01] develops a theory of
 generalized multicategories in such a context.
 Let K be a finitely complete 2-category (see [Str76]). Since its underlying ordinary
 category K0 has pullbacks, we can form the virtual equipment Prof(K0). Now, as observed
 in [Str74], for any object A ∈ K we have an internal category ΦA in K, defined by
 (ΦA)0 = A and (ΦA)1 = A2 (the cotensor with the arrow category 2). Similarly, every
 morphism f: A B defines aninternal functor Φf: ΦA ΦB, and the same for 2-cells;
 thus we have a 2-functor K
 V(Prof(K0)). Moreover, this 2-functor is locally full and
 faithful, i.e. 2-cells f
 g are in bijection with internal natural transformations Φf
 Φg.
 We define an internal profunctor ΦA H ΦB to be a discrete fibration from A to
 B if the object H ∈ K/(A×B) is internally discrete, i.e. (K/(A×B))(C,H) is a discrete
 category for any C ∈ K/(A×B). We define DFib(K) to be the sub-virtual double category
 of Prof(K0) determined by
69
 • The internal categories of the form ΦA,
 • The internal functors of the form Φf,
 • The internal profunctors which are discrete fibrations, and
 • All cells between these.
 Since the pullback of a discrete fibration is a discrete fibration, and UΦA is a discrete
 f
 ibration, DFib(K) is a virtual equipment. Our remarks above show that K ≃ V(DFib(K)).
 Under suitable conditions on K, discrete fibrations can be composed, so that DFib(K)
 becomes an equipment. (Several authors have tried to isolate these conditions, with
 varying degrees of success; in addition to [Her01] see [Str80] and [CJSV94]. Our approach
 sidesteps this issue completely.)
 Now suppose that F : K
 L is a 2-functor that preserves pullbacks and comma ob
jects. Then it preserves internal categories, profunctors, the Φ construction, and discrete
 f
 ibrations, so it induces a normal functor DFib(F): DFib(K)
 2-natural transformation F
 DFib(L). Likewise, any
 G induces a transformation DFib(F)
 DFib(G), so we
 have a 2-functor DFib from finitely complete 2-categories to vEquip. In particular, any
 2-monad T on K whose functor part preserves pullbacks and comma objects induces a
 normal monad on DFib(K), so we can talk about DFib(T)-monoids.
 This is basically the context of [Her01], except that, like most other authors, he works
 only with bicategories. Thus, he assumes that K has the structure required to com
pose discrete fibrations, and that moreover T preserves this structure and that µ and η
 are cartesian transformations. This ensures that DFib(T) is horizontally strong, so that
 H-Kl(DFib(K),DFib(T)) is an equipment. Under these hypotheses, we have:
 B.15. Theorem. The 2-category nKMon(DFib(K),DFib(T)) of normalized DFib(T)
monoids is isomorphic to the 2-category Lax-Bimod(T)-alg defined in [Her01, 4.3 and
 4.4].
 Our Theorem 9.2 is also a generalization of results of [Her01]. Hermida proves fur
thermore that under his hypotheses, the left adjoint FT from Remark 9.16 exists, the
 adjunction is monadic when restricted to pseudo T-algebras, and the induced monad T⊣
 on Lax-Bimod(T)-alg is lax-idempotent (see [KL97]). In [CS10b] we will show that an
 analogous result is true for any monad T on an equipment X satisfying suitable cocom
pleteness conditions.
 B.16. Monoidal pseudo algebras. In [Web05], Weber gives a definition of gener
alized operads enriched in monoidal pseudo algebras. More precisely, for any 2-monad
 T on a 2-category K with finite products, and any pseudo T-algebra A which is also
 a pseudomonoid in a compatible way, he defines a notion of T-operad in A. A general
 description of the relationship of this theory to ours would take us too far afield, so we
 will remark only briefly on how such a comparison should go.
 For any pseudomonoid A in a 2-category K with finite products, there is a virtual
 equipment A-Mat defined as follows. Its objects and vertical arrows are the objects and
70
 arrowsofK.AhorizontalarrowfromX Y isamorphismX×Y p AinK,anda
 cell
 X0
 p1
 f
 X1 _ _ _ Xn−1
 pn Xn
 g
 Y0 q Y1
 isa2-cell
 Y0×Y1 A. q
 (X0×X1)×(X1×X2)×···×(Xn−1×Xn)
 Y0×Y1
 (f,g)
 •••••••••
 (X0×X1)×(X1×X2)×···×(Xn−1×Xn)
 A.
 (p1⊗···⊗pn)
 ? ? ? ? ? ? ? ? ?
 oo oo
 inK,where⊗:A×A AisthemultiplicationofthepseudomonoidA(ifn=0weuse
 itsunit instead).
 Now, ifAisadditionallyapseudoT-algebrainacompatibleway,wemighthopeto
 beabletoextendTtoamonadonA-Mat.However,givenahorizontalarrowX p Y,
 fromX×Y p Awecanformthecomposite
 T(X×Y) Tp TA a A,
 but this isnotyetahorizontal arrowTX TY. Ifweassume thatAadmitswell
behavedleft (Kan)extensions, thenwecandefineTX Tp TY tobetheextensionof
 theabovecompositealongT(X×Y) TX×TY.WecanthenconstructH-Kl(A-Mat,T)
 andKMod(A-Mat,T)asusual.Moreover,wecangiveanequivalentcharacterizationof
 H-Kl(A-Mat,T)whichisvalidevenintheabsenceof leftextensions: ahorizontalarrow
 X Y isamorphismX×TY p AinK,andacell
 X0
 p1
 f
 X1 _ _ _ Xn−1
 pn Xn
 g
 Y0 q Y1
 isa2-cell
 X0×T(X1×...T(Xn−1×TXn)...)
 π p1⊗...⊗pn
 U U U U U U U U U U U U U U U U U U U U
 X0×TnXn
 1×µn−1
 A
 X0×TXn
 f×Tg
 Y0×TY1
 q
 s s s s s s s s s s s s s s s s s s s s s s s s s s
71
 in K. Thus, we obtain a notion of T-monoid in A for any monoidal pseudo algebra A.
 Weber only considers the case of operads, rather than more general multicategories, but
 it is easy to verify that his T-operads in A coincide with those T-monoids in A whose
 underlying object in K is the terminal object 1.
 Actually, there is a good reason that Weber considers only operads: T-monoids
 X0
 X TX0 in this context for which X0 is not discrete, or at least a groupoid, are
 not very familiar objects. In familiar cases such as K = Cat, we would obtain familiar
 types of A-enriched multicategory only by taking the horizontal arrows X
 Y in A-Mat
 to be morphisms X × Yop
 A, rather than X × Y
 A. To put this in a general
 context, however, requires a 2-category K in which “opposites” make sense, such as the
 “2-toposes” of [Web07].




 Recursive Neural Networks
 Sargur Srihari
 srihari@buffalo.edu
 1 
Deep Learning                                                                               
Topics
 Srihari 
• Sequence Modeling: Recurrent and Recursive Nets
 1. Unfolding Computational Graphs
 2. Recurrent Neural Networks
 3. Bidirectional RNNs
 4. Encoder-Decoder Sequence-to-Sequence Architectures
 5. Deep Recurrent Networks
 6. Recursive Neural Networks
 7. The Challenge of Long-Term Dependencies
 8. Echo-State Networks
 9. Leaky Units and Other Strategies for Multiple Time Scales
 10. LSTM and Other Gated RNNs
 11. Optimization for Long-Term Dependencies
 12. Explicit Memory
 2 
Deep Learning                                                                               
Srihari 
Recursive Neural Networks
 • They are yet another generalization of recurrent networks with 
a different kind of computational graph
 • It is structured as a deep tree, rather than the chain structure of 
RNNs
 • The typical computational graph for a recursive network is 
shown next
 3 
Deep Learning                                                                               
Srihari 
Computational graph of a Recursive Network
 • It generalizes  a recurrent 
network from a chain to a tree
 • A variable sequence x(1),x(2),,x(t) 
can be mapped to a fixed size 
representation (the output o), with 
a fixed set of parameters (the 
weight matrices U,V,W)
 • Figure illustrates supervised 
learning case in which target y is 
provided that is associated with 
the whole sequence
 4 
Deep Learning                                                                               
Srihari 
Advantage of Recursive over Recurrent Nets
 • For a sequence of the same length τ, the depth (measured as 
the no. of compositions of nonlinear operations) can be reduced 
from τ to O(log τ), which might help deal with long-term 
dependencies
 • An open question is how best to structure the tree
 5 
Deep Learning                                                                               
Srihari 
Need for Recursive nets in NLP
 • Deep learning based methods learn low-dimensional, real
valued vectors for word tokens, mostly from a large data 
corpus, successfully capturing syntactic and semantic 
aspects of text
 • For tasks where the inputs are larger text units, e.g., 
phrases, sentences or documents, a compositional model 
is first needed to aggregate tokens into a vector with fixed 
dimensionality that can be used for other NLP tasks
 • Models for achieving this fall into two categories: recurrent 
models and recursive models
 6 
Deep Learning                                                                               
Srihari 
Recurrent Model for NLP
 • Recurrent models deal successfully with time series data
 • The recurrent models generally consider no linguistic structure 
aside from the word order
 • They were applied early on to NLP by modeling a sentence as 
tokens processed sequentially and at each step combining the 
current token with previously built embeddings
 • Recurrent models can be extended to bidirectional ones from 
both left to right and right to left
 • These models consider no linguistic structure aside from word 
order
 7 
Deep Learning                                                                               
Srihari 
Recursive Models for NLP
 • Recursive neural models (also referred to as tree models) by 
contrast are structured by syntactic parse trees
 • Instead of considering tokens sequentially, recursive models 
combine neighbors based on the recursive structure of parse 
trees, starting from the leaves and proceeding recursively in a 
bottom-up fashion until the root of the parse tree is reached
 • Ex: for the phrase the food is delicious, following the operation sequence 
((the food) (is delicious)) rather than the sequential order (((the food) is) 
delicious) 
8 
Deep Learning                                                                               
Srihari 
Advantage of Recursive Model for NLP
 • They have the potential of capturing long-distance 
dependencies
 • Two tokens may be structurally closer to each other even 
though they are far away in word sequence
 • Ex: a verb and its corresponding direct object can be far away 
in terms of tokens if many adjectives lie inbetween, but they are 
adjacent in the parse tree
 • However parsing is slow and domain dependent
 • See performance comparison with LSTM on four NLP tasks  at 
https://nlp.stanford.edu/pubemnlp2015_2_jiwei.pdf 
9 
Deep Learning                                                                               
Srihari 
Structure of the Tree
 • One option is to have a tree structure that does not depend on 
the data, such as a balanced binary tree
 • In some application domains, external methods can suggest the 
appropriate tree structure
 • Ex: when processing natural language sentences, the tree structure for 
the recursive network can be fixed to the structure of the parse tree of 
the sentence provided by a natural language parse
 • Ideally, one would like the learner itself to discover and infer the 
tree structure that is appropriate for any given input
 10 
Deep Learning                                                                               
Srihari 
Variants of Recursive Net idea
 • Associate data with a tree structure and associate inputs and 
targets with individual nodes of the tree
 • The computation performed for each node does not have to be the 
artificial neuron computation (affine transformation of all inputs followed 
by a monotone nonlinearity)
 • Can use a tensor operations of bilinear forms
 • Previously found useful to model linear relationships between 
concepts when the concepts are represented by continuous vectors
 11 
Deep Learning                                                                               
Srihari 
Recursive Neural Networks 
• Recursive neural networks 
are also called Tree Nets 
• Useful for learning tree-like 
structures
 • They are highly useful for 
parsing natural scenes and 
language
 12 
Deep Learning                                                                               
Srihari 
Unrolling Recurrent and Tree Nets
 • In RNNs, at each time step the network takes as input its 
previous state s(t-1) and its current input x(t) and produces an 
output y(t) and a new hidden state s(t). 
• TreeNets, on the other hand, don’t have a simple linear 
structure like that. 
• With RNNs, you can ‘unroll’ the net and think of it as a large 
feedforward net with inputs x(0), x(1), …, x(T), initial state s(0), 
and outputs y(0),y(1),…,y(T), with T varying depending on the 
input data stream, and the weights in each of the cells tied with 
each other. 
• You can also think of TreeNets by unrolling them – the weights 
in each branch node are tied with each other, and the weights 
in each leaf node are tied with each other. 
13 
Deep Learning                                                                               
Srihari 
Advantage of Recursive Nets
 • The advantage of Recursive Nets is that they can be very 
powerful in learning hierarchical, tree-like structure. 
• The disadvantages are, firstly, that the tree structure of every 
input sample must be known at training time



Thinking Recursively, Rethinking Corecursively
 David Jaz Myers
 June 19, 2017
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Mathematical Metaphors
 This talk will be about two specific mathematical metaphors, but
 what are mathematical metaphors,
 why make them,
 and how can they be misused?
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Mathematical Metaphors
 In this talk, we will look closely at the mathematical metaphor
 between
 Complex Systems and Recursive Functions
 Wewill see how this metaphor a lot of standard theories in science
 and philosophy, usually those that fall under the rubrik of “realism”.
 Wewill also find that this metaphor can lead us to some shaky
 philosophical positions.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 What is a function
 A function is a process that turns an input into an output.
 F(input) = output
 If a function takes inputs of a type Inputs and gives outputs of a
 type Outputs, we write
 F : Inputs Outputs
 For example,
 F : Numbers Numbers
 F(n) = 2n +1
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 What is Recursion?
 A function is recursive when its output on a complicated input is
 determined by its output on simpler inputs.
 Ultimately, the output of a recursive function is determined by its
 simplest inputs.
 Wecall these simplest inputs atoms, or base cases, and the rules
 for building them up constructors.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 What is Recursion?
 So to define a recursive function we need
 to know how to break apart complicated inputs into simpler
 ones,
 simplest inputs (so we eventually stop breaking things apart),
 to know how to put outputs together in a way that relates to
 taking inputs apart!
 Or, more pithily, we need:
 to know how to analyze inputs,
 into their atomic components,
 so that we can construct outputs.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 A Lengthy Example
 Let’s calculate the length of a list! This is a function which takes a
 list as input and gives a number as output.
 Length : Lists Numbers
 A list is something like:
 [first item, second item, third item
 Wecan break down a list like this:
 last item]
 AList = [first item, Rest of the List]
 or the list is Empty.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 A Lengthy Example
 Let’s calculate the length of a list! This is a function which takes a
 list as input and gives a number as output.
 Length : Lists Numbers
 Numbers can be built up by counting:
 0 is a number, and
 (1 +anumber) is a number.
 This is related to taking lists apart because, secretly, numbers are
 like lists of tally marks:
 4 =
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 A Lengthy Example
 Definition (Length of a List)
 The length of a list is given by the function defined by:
 Length(Empty) 0
 Length([first itemRest of List]) 1 + Length(Rest of List)
 This works because
 Empty is an atom. There are no simpler lists, so we can stop
 breaking things apart.
 The Rest of the List is simpler (i.e. smaller) than the list we
 started with. This means we eventually get to the Empty list.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Running a Recursive Program
 Wecan run a recursive program greedily:
 Every time we see something we don’t understand, we compute it.
 Length([123]) = 1+Length([23])
 =1+(1+Length([3]))
 =1+(1+(1+Length(Empty)))
 =1+(1+(1+0))
 =1+(1+1)
 =1+2
 =3
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Thinking Recursively About Everything
 This way of thinking should be familiar to you from popular ways of
 thinking about physics.
 Claim
 Physics is like a recursive function
 Physics : Systems Systems
 which recurses all the way to the fundamental particles, and then
 builds more complicated phenomena out of the way they behave.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Thinking Recursively About Everything
 Or from philosophy of language:
 Claim
 Meaning is like a recursive function
 Meaning : Utterances Meanings
 which builds the meaning of, say, sentences out of the meaning of
 words.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Thinking Recursively About Everything
 Or from sociology
 Claim
 A society is like a recursive function
 Society : Societies 
Societies
 which is determined by the behavior of individuals which are, of
 course, indivisible.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Thinking Recursively About Everything
 Or from economics
 Claim
 The economy is like a recursive function
 Economy : Markets Markets
 which is determined by the behavior of agents who act rationally.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Analysis is Recursive
 Definition
 [Analysis] might be defined as a process of isolating or
 working back to what is more fundamental by means of
 which something, initially taken as given, can be
 explained or reconstructed.– Stanford Encyclopedia
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 A Philosophical Problem
 In his book The Case for Idealism, John Foster argues that some
 things must have inscrutable, intrinsic properties.
 Foster’s argument for inscrutable intrinsic properties
 Suppose that all properties of all things were extrinsic, that is,
 defined in relation to other things.
 A)
 (B
 Now, consider a world containing two things, A and B, each
 defined only by their disposition to repel the other.
 Foster claims this leads to an infinite regress, and therefore a
 contradiction.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 A Philosophical Problem
 Foster’s argument for inscrutable intrinsic properties (cont’d)
 The back and forth must stop somewhere:
 “A is the thing which 
X”
 X is the end of the line, it is not defined in relation to anything else.
 Therefore, it is both
 inscrutable, and
 intrinsic.
 This argument rests on two (recursive) assumptions:
 1 Wemust ‘evaluate’ greedily.
 2 There must be a base case.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Do WeHaveto Make Those Assumptions?
 is there another way?
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Corecursion
 A function is corecursive when its output is determined by simpler
 outputs.
 Wecall the rules for breaking apart the output observers.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 What is Corecursion
 So, to define a corecursive function we need
 to know how to observe the output of our function in simpler
 ways,
 that relate to how we observe our inputs!
 Wecan think of the observers as being experimental setups with
 which we will test the output of our function.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 What is Corecursion
 The main idea behind corecursion is:
 If we know how our function behaves in all experimental
 setups, we know what it does.
 This is essentially the same as one of the fundamental principles
 of science:
 If we can predict how something behaves in all experimental
 setups, then we know what it is.
 So long as we believe that a function is what it does.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Stream and Chill
 Let’s have some fun with streams to get our heads around
 corecursion.
 A stream is an infinite list, so we can’t keep the whole thing in
 memory, but we can observe it piece by piece.
 So, let’s set up two experiments:
 1 Head, where we test what the first thing in the stream is.
 2 Tail, where we see what’s left.
 Now wecan define functions corecursively, since we know how to
 observe their behavior.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Stream and Chill
 Let’s define a function
 Every Other : Streams Streams
 that will take a stream and return the stream of only every other
 value. For example:
 Every Other(01234 )=(024 )
 To define this, we just need to define how it looks in all the
 experiments.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Stream and Chill
 Definition (The Every Other Function)
 Define the Every Other function by
 EO(stream)Head = streamHead
 EO(stream)Tail = EO(streamTailTail)
 This works because
 EO(stream) is covered by the observers Head and Tail, they
 tell us all we need to know about it.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Running a Corecursive Program
 Wecan’t evaluate a corecursive program greedily, because the
 calculation would never end! We have to be lazy:
 Only compute things when we absolutely need to.
 So if you wrote down
 EO((0123 ))
 That would be totally chill.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Running a Corecursive Program
 But, if we want to know a specific value of EO((0123 )), then
 we can calculate
 EO((0123 ))TailTailHead
 =EO((0123 )TailTail)TailHead
 =EO((0123 )TailTailTailTail)Head
 =(0123 )TailTailTailTailHead
 =(1234 )TailTailTailHead
 =(2345 )TailTailHead
 =(3456 )TailHead
 =(4567 )Head
 =4
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Corecursion and Diff´ erance
 If someone asks you what “EO” means, you could tell them that its
 meaning is deferred until we test it with the observers Head and
 Tail.
 If they ask you what “Head” and “Tail” mean, you could only tell
 them the different ways you end up using them.
 Definition
 Diff´ erance is Derrida’s pun on the words defer and differ.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Thinking Corecursively
 Who amI?
 How can I find out?
 Do I have to find my ‘true self’, the core of my being, to know who I
 am?
 Or do I only have to look at the way I affect the people and places
 around me?
 Thinking corecursively, we don’t have to be anxious about finding
 our true selves.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Revisiting Foster
 Let’s look back at Foster’s argument for inscrutable intrinsic
 properties. He claims that the world in which
 A only repels B and B only repels A
 cannot exist because it leads to an infinite regress.
 Only leads to infinite regress if we are greedy.
 If we are lazy, this is a perfectly fine definition.
 There is nothing inscrutable about it.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Revisiting Foster
 Foster’s argument shows a fundamental confusion that often
 underlies recursive thinking:
 the confusion between names and things
 Names are like atoms, we don’t break them apart.
 Things (such as functions) can be named, even when we
 define them corecursively.
 But that doesn’t mean that they have base cases!
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Limits of the Metaphor
 To define a function corecursively, we must cover it by observers.
 Head and Tail tell us all there is to know about a stream.
 But in the informal world, we never have access to all the contexts
 in which an object appears,
 Wecan never get all sides of the story.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Going Forward: Physics
 Physicists have been thinking corecursively for a long time:
 A physical quantity can only be assigned specific values given
 a local coordinate system, or gauge.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Going Forward: Physics
 Principle of Relativity
 The physical laws have the same form in all choices of gauge.
 A change in gauge is called a gauge symmetry.
 In other words, if we rotate our experimental setup, we get a
 rotated result.
 r(X) = r( X)
 The relationship between the observations X and r(X)
 depends on how X was rotated to r(X).
 To fully know an object, we must not only know how it behaves in
 various contexts,
 we must also know how those contexts relate.
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 In Conclusion
 Thinking recursively makes us believe that
 There are basic objects and basic truths about them at the
 bottom of all phenomena, and
 To know anything at all, we need to know about these basic
 things.
 Thinking corercursively makes us believe that
 Things only make sense in context (in an experiment, relative
 to an observer, etc.), and
 Knowing how a thing behaves in context is all there is to know
 about it
 There are no basic objects or basic truths
 David Jaz Myers
 Thinking Recursively, Rethinking Corecursively
What is Recursion?
 Thinking Recursively
 There is Another Way
 Thinking Corecursively
 Bridging the Divide
 In this talk, I made a stark division between recursive and
 corecursive thinking.
 But in actually programming languages (like Haskell), you can use
 recursion and corecursion together depending on which is more
 convenient.
 Weshould use recursive and corecursive thinking together,
 depending on what needs to be done.
 But most importantly, we need to remember that metaphors matter.
 Don’t get trapped in a single metapho



 Dirichlet Functors are Contravariant Polynomial Functors
David Jaz Myers David I. Spivak
April 2020
Abstract
Polynomial functors are sums of covariant representable functors from the category
of sets to itself. They have a robust theory with many applications — from operads and
opetopes to combinatorial species. In this paper, we define a contravariant analogue
of polynomial functors: Dirichlet functors. We develop the basic theory of Dirichlet
functors, and relate them to their covariant analogues.
1 Introduction
A polynomial functor P : Set → Set is a sum of representables
P(X) := X
b∈B
XEb (1)
where the family of sets Eb depends on b ∈ B. This data is known in the computer
science literature as a “container” [2, 3, 1], but since such an indexed family of sets can
be represented by as a function
E
B
π
we will refer to it as a bundle.
Remarkably, all natural transformations between polynomial functors can be represented in terms of their associated bundles. A natural transformation P → P
′
corresponds
to a dependent pair of functions

f : B → B
′
, f♯
: (b : B) → E
′
fb → Eb

noting that f acts covariantly on the base and f
♯ acts contravariantly on fibers. In terms
of bundles, a map π → π
′
is a diagram of the following sort:
E • E′
B B B′
π
f♯
p
π
′
f
We refer to these special spans as contravariant morphisms of bundles.
1
Theorem 1.1 (Theorem 2.17 of [4]). The category of polynomial functors and natural
transformations is equivalent to the category of bundles and contravariant morphisms.
This begs the question: what, then, are we to make of the more obvious, covariant
morphisms of bundles
E E′
B B′
tot(f♯)
π π
′
f
for which f♯
is covariant in each fibers?
It turns out that these covariant maps of bundles correspond to natural transformations
between the appropriate sums of contravariant representables:
D(X) := X
b∈B
E
X
b
.
Polynomial functors as in (1) get their name from the case in which B and E are
finite sets. Consider the function card E(−)
: B → N, which takes the cardinality of each
fiber Eb. Letting Bn := (cardE(−)
)
-1(n), i.e. Bn is the set of elements whose fibers have n
elements, we find that the for any set X, the cardinality
|P(X)| =
X
n∈N
|Bn||X|
n
is a polynomial in the cardinality of X. Similarly,
|D(X)| =
X
n∈N
|Bn|n
|X|
resembles a Dirichlet series in the cardinality of X – without the usual negative sign.1
Accordingly, we call such sums of contravariant representables Dirichlet functors.
We will show in this paper that Dirichlet functors are, quite robustly, the contravariant
analogue of polynomial functors. In particular, the many equivalent ways to say that a
functor is polynomial have contravariant analogues.
Theorem 1.2 (See discussion in 1.18 of [4]). Let P : Set → Set be a functor. Then the
following are equivalent.
1. P is polynomial.
2. P is the sum of covariant representables.
3. There is a bundle π : E → B together with a natural isomorphism
P(X) ∼=
X
b∈B
XEb
.
1Future work of the first author will recover the negative sign by generalizing the theory of Dirichlet
functors to homotopy types.
2
Or, equivalently, a natural isomorphism of P with the composite
Set
∆!E −−→ Set/E
Ππ −−→ Set/B
Σ!B −−→ Set.
4. P is accessible and preserves connected limits.
Analogously, we will prove the following theorem.
Theorem 1.3. Let D : Set op → Set be a contravariant functor. Then the following are
equivalent.
1. D is Dirichlet.
2. D is the sum of contravariant representables.
3. There is a bundle π : E → B together with a natural isomorphism
D(X) ∼=
X
b∈B
E
X
b
.
Or, equivalently, a natural isomorphism of D with the composite
Set op
(∆!B
)
op
−−−−−→ (Set/B)
op
Set/B(−,π)
−−−−−−−→ Set/B
Σ!B −−→ Set.
4. D preserves connected limits.
Note that we no longer need to assume accessiblity. This is a general feature of the
theory of Dirichlet functors; it is a bit “smaller” and more manageable than that of
polynomials. In particular, a Dirichlet functor is determined by its action on the terminal
morphism !0 : 0 → 1 of the empty set. As a corollary, Dirichlet functors form a topos.
Theorem 1.4. The functor Set↓ → Fun(Set op
, Set), given by sending π : E → B to the
induced Dirichlet functor X 7→
P
b∈B EX
b
, is fully faithful, and so gives an equivalence
Set↓ ≃ Dir
between the topos of bundles and the category of Dirichlet functors, with inverse given by
evalutation at !0 : 0 → 1.
Now, object-wise, a Dirichlet functor and a polynomial functor are determined by the
same data — a bundle π : E → B of sets. Accordingly, one would expect for any set N a
transformation
XN 7→ N
X
turning polynomial functors into Dirichlet functors, and vice versa. But the natural transformations between each sort of functor induce different morphisms between the bundles;
natural transformations between polynomial functors induce contravariant bundle morphisms, while natural transformations between Dirichlet functors induce covariant bundle
3
morphisms. However, if we restrict to those morphisms of bundles which are isovariant
on the fibers — that is, the pullback diagrams of the form
E E′
B B′
tot(f♯)
π
p
π
′
f
which preserve the number of elements in each row — we find that such a morphism is
both a co- and contravariant morphism of bundles. It is well known that such cartesian
morphisms of bundles correspond to cartesian natural transformations between polynomial
functors [4, Theorem 3.8] — those whose naturality squares are pullbacks. This is true as
well for Dirichlet functors.
Theorem 1.5. A natural transformation D → D′ of Dirichlet functors is Cartesian if
and only if the corresponding bundle map
E E′
B B′
tot(f♯)
π
p
π
′
f
is a pullback. As a corollary, we have an equivalence of categories
Polyp ≃ Dirp
between polynomial functors with cartesian natural transfromations and Dirichlet functors
with cartesian natural transfromations.
Acknowledgements. We appreciate helpful comments from Andr´e Joyal and Joachim
Kock on an early draft of this paper. Myers was supported by the National Science
Foundation grant DMS-1652600, and Spivak was supported by AFOSR grants FA9550-
19-1-0113 and FA9550-17-1-0058.
2 Dirichlet Functors
Before diving in to the theory of Dirichlet functors, let’s first consider the category Set↓
of bundles of sets and covariant bundle maps. For our proofs to go smoothly, we will need
to explicitly keep track of the self-dualizing isomorphism ↓
∼−→ (↓)
op on the walking arrow.
Definition 2.1. We let ↓ be the walking arrow — the category dom → cod consisting of
a single morphism. We denote by σ : ↓ → (↓)
op the self-dualizing isomorphism of ↓, and
note that σ
-1 = σ
op
.
4
Proposition 2.2. There is an adjoint sextuple:
Set Set const ↓
cod
dom
!
(−)
!(−)
ZC
All three functors Set → Set↓
are fully faithful.
Proof. There is an adjoint triple 1 ↓ . The middle three functors—cod, const, and
dom—are given by restricting along this adjoint triple. The next two, !(−) and !(−)
, are
given by Kan extending, or more concretely:
X 7→
0
X
!X and X 7→
X
1
!X
(2)
It is easy to see that the unit X → dom!X is an isomorphism (it is in fact an identity), so
!(−)
is fully faithful. Therefore, all three functors going from Set → Set↓
are fully faithful.
The existence of the final adjoint can be deduced from the fact that !(−) preserves
all limits. It sends a bundle π : E → B to the largest subset ZC(π) of B for which the
following square is a pullback
0 E
ZC(π) B
p
π
We prove a few quick facts we will use later.
Lemma 2.3. The functor !(−)
: Set → Set↓
from (2) preserves connected colimits.
Proof. To see that !(−) preserves connected colimits, recall that colimits in Set↓
are calculated pointwise. It remains to show, then, that the map of bundles
colim Xi colim Xi
colim 1 1
is an isomorphism in Set↓
, for which it suffices to show that colim 1 is terminal. But the
colimit of a diagram of terminal objects is the set of connected components of its indexing
category. Since we assumed the indexing category was connected, this contains a single
element.
5
Lemma 2.4. The Yoneda embedding y : (↓)
op → Set↓
is equal to the composite
(↓)
op σ
op
−−→ ↓ !0−→ Set
!(−)
−−→ Set↓
.
As a corollary, any π :↓→ Set is naturally isomorphic to the composite
↓
σ−→ (↓)
op !0
op
−−→ Set op
!(−)
op
−−−−→ (Set↓
)
op Set↓
(−,π)
−−−−−−→ Set
by the Yoneda lemma.
Proof. One checks directly.
Now we will define the extent of a bundle π to be the Dirichlet functor extπ : Set op →
Set that it corresponds to. This sends a bundle π : E → B to the functor
extπ(X) :=
X
b∈B
E
X
b
.
We will, however, give a more abstract definition of the extent, and then calculate a
number of presentations of it.
Definition 2.5. Consider the functor !0
op ◦σ : ↓ → Set op picking out the unique morphism 1 → 0 in Set op. Sending a functor Set op → Set to its precomposition with !0
op ◦σ
gives an evaluation functor
Fun(Set op
, Set)
ev!0 −−→ Set↓
.
This functor admits a right adjoint by right Kan extension along !0
op ◦σ : ↓ → Set op; we
define the Dirichlet extent functor ext : Set↓ → Fun(Set op
, Set) to be this right adjoint. It
sends any bundle π to
extπ :≡ ran!0
op ◦σπ.
Proposition 2.6. Let π : E → B be a bundle. The following are equivalent:
1. The extent extπ : Set op → Set of π from Definition 2.5.
2. The functor
X 7→
X
b∈B
E
X
b
,
or equivalently the composite
Set op (∆B)
op
−−−−−→ (Set/B)
op
Set/B(−,π)
−−−−−−−→ Set/B
ΣB −−→ Set.
3. The pullback in Fun(Set op
, Set):
extπ B
Set(−, E) Set(−, B)
p
6
4. The restricted representable functor Set↓
(!(−)
, π).
5. The functor
X 7→ lim(HomSet(!0, X)
op → ↓ op σ
op
−−→ ↓ π−→ Set)
where HomSet(!0, X) is the comma category of !0 : ↓ → Set over X : ∗ → Set.
6. The functor
X 7→ lim((X
⊳
)
op (!⊳
)
op
−−−−→ (1⊳
)
op σ
op
−−→ ↓ π−→ Set)
where (−)
⊳
is the left cone 2-functor, adjoining an initial object.
Proof. We have presented these results in order of most understandable to most computational; we will prove it a somewhat opposite order.
First, we note that the conical limit formula for extπ ≡ ran!0 π as a right Kan extension
says
extπ(X) = lim(HomSet op(X, !0
op ◦σ) → ↓ π−→ Set).
Now, HomSet op(X, !0
op ◦σ) ≃ HomSet(!0 ◦ σ
op, X)
op over ↓. Furthermore, we have the
following equivalence:
HomSet(!0 ◦ σ
op, X)
op ↓
HomSet(!0, X)
op ↓
op
∼ σ
and therefore we may equivalently calculate this limit as
lim(HomSet(!0, X)
op → ↓ op σ
op
−−→ ↓ π−→ Set).
This gives us the equivalence between (1) and (5).
The comma category HomSet(!0, X) simply adjoins an initial object to (the discrete
category) X. Therefore, we find that (5) and (6) are equivalent.
Every set X is the colimit of the diagram X⊳
1
⊳
−→ ↓ !0−→ Set, namely:
X
1 1 · · · 1 1
0
Since, by Lemma 2.3, !(−) preserves connected colimits, we may make the following identification of (4) with (6) using Lemma 2.4:
Set↓
(!X , π) = Set↓
(!
colim(X⊳
!⊳
−→1
⊳
!0−→Set)
, π)
≃ Set↓
(colim(X
⊳ !
⊳
−→ 1
⊳ !0−→ Set
!(−)
−−→ Set↓
), π)
≃ lim((X⊳
)
op (!⊳)
op
−−−−→ (1⊳
)
op !0
op
−−→ Set op
!(−)
op
−−−−→ (Set↓
)
op Set↓
(−,π)
−−−−−−→ Set)
≃ lim((X⊳
)
op (!⊳)
op
−−−−→ (1⊳
)
op σ
op
−−→ ↓ π−→ Set).
7
We see that (3) is equivalent to (4) by noting that the following square of natural
transformations is a pullback:
Set↓
(−, −) Set(cod(−), cod(−))
Set(dom(−), dom(−)) Set(dom(−), cod(−))
p
and restricting the right side to π and the left side to !(−)
.
Finally, we note that the set Set↓
(!X , π) is naturally isomorphic to the set P
b∈B EX
b
,
letting us identify (4) with (2).
Now we are ready to intrinsically characterize the Dirichlet functors.
Definition 2.7. A Dirichlet functor is a contravariant functor D : Set op → Set which
preserves connected limits. We denote by Dir the category of Dirichlet functors and natural
transformations.
Theorem 2.8. The functor ext is fully faithful, and gives an equivalence
Set↓ ≃ Dir .
As a corollary, the category of Dirichlet functors is a topos.
Proof. Since !0 : ↓ → Set op is fully faithful, the counit of the ev!0 ⊢ ext adjunction,
the universal cell defining the right Kan extension ext−, is an isomorphism. Thus ext is
fully faithful. In what follows we show that a functor is Dirichlet—preserves connected
limits—if and only if it is the extent of a bundle, proving the equivalence of Dir with Set↓
.
If D is the extent of a bundle π, then by Prop 2.6, D is naturally isomorphic to the
restricted representable Set↓
(!(−)
, π). By Lemma 2.3, this sends connected colimits in Set
to connected limits.
Now, we show that if D is Dirichlet, then the unit D → extD!0
is an isomorphism. By
Prop 2.6,
extD!0
(X) = lim(X
⊳ !
⊳
−→ 1
⊳ D!0 −−→ Set).
Every set X is the connected colimit of the diagram X⊳ → ↓ !0−→ Set, and therefore if D
preserves this limit, then D(X) is precisely the above limit extD!0
(X).
Remark 2.9. Since polynomial functors preserve connected limits, the composite P ◦ D
of a polynomial functor after a Dirichlet functor is Dirichlet. On the other hand, the
composite D′ ◦D op of two Dirichlet functors does not in general preserve connected limits,
since D op sends connected colimits in Set to connected colimits in Set op, and D′ does not
necessarily preserve these. Furthermore, composites of Dirichlet functors are not in general
accessible.
8
Remark 2.10. The six adjoints of Proposition 2.2 correspond, under the equivalence of
Theorem 2.8, to
ZC(D!0) ∼= the coefficient of 0X in D.
ext(!C
) ∼= X 7→ C × 0
X
cod(D!0) ∼= D(0)
ext(const(C)) ∼= X 7→ C
dom(D!0) ∼= D(1)
ext(!C) ∼= X 7→ C
X
In particular, !(−) corresponds to the Yoneda embedding.
3 Cartesian Transformations between Dirichlet Functors
In this section, we turn to cartesian transformations between Dirichlet functors. We will
show that the category of Dirichlet functors and cartesian transfromations is equivalent
to the category of polynomial functors and cartesian transformations.
Proposition 3.1. A natural transformation φ : D → D′ between Dirichlet functors is
cartesian if and only if the induced bundle map D!0 → D′
!0 is a pullback.
As a corollary, the equivalence Dir ≃ Set↓
restricts to an equivalence
Dirp ≃ Set↓
p
between Dirichlet functors with cartesian natural transformations and bundles with pullback squares.
Proof. We want to show that for any f : D → D′
, the square
D(1) D′
(1)
D(0) D′
(0)
f1
π π
′
f0
(3)
is a pullback in Set iff for all functions g : X → X′
, the naturality square
D(X′
) D′
(X′
)
D(X) D′
(X)
fX′
D(g) D′
(g)
fX
(4)
is a pullback in Set. We will freely use the natural isomorphism D(X) ∼= Set↓
(!X , D!0)
from Proposition 2.6, which allows us to identify Diagram (4) with
Set↓
(!X′ , D!0) Set↓
(!X′, D′
!0)
Set↓
(!X , D!0) Set↓
(!X , D′
!0)
f!0,1
!
1
g
!
1
g
f!0,1
(5)
9
The square in Diagram (3) is a special case of that in Diagram (4), namely for g :=!0;
this establishes the only-if direction.
To complete the proof, suppose that Diagram (3) is a pullback, take an arbitrary
g : X → X′
, and suppose given a commutative solid-arrow diagram as shown:
X X′
D(1) D′
(1)
1 1
D(0) D′
(0)
g
We can interpret the statement that Diagram (5) is a pullback as saying that there are
unique dotted arrows making the diagram commute. So, we need to show that if the front
face is a pullback, then there are unique diagonal dotted arrows as shown, making the
diagram commute. This follows quickly from the universal property of the pullback.
Theorem 3.2. There is an equivalence of categories
Polyp ≃ Dirp
between the category of polynomial functors and cartesian transformations and Dirichlet
functors and cartesian transformations. This equivlalence sends representables to representables
(−)
N 7→ N
(−)
.
Proof. This follows by composing the equivalence of Dirp with Set↓
from Proposition 3.1
with that of [4, Proposition 3.14], noting that Set↓
p
is the category of (1, 1)-polynomials.
Corollary 3.3. Let D be a Dirichlet functor. Then the category Dirp/D of Dirichlet
functors with a cartesian map to D is a topos.
Proof. By Theorem 3.2, this category is equivalent to Polyp/P for a polynomial P. But
this is a topos as observed in [5, Remark 2.6.2].
Now, since Dir is a topos, so is Dir/D. And, as we saw above, Dirp/D is a topos as well.
What is the relationship between Dir/D and Dirp/D?
We will show that Dir/pD is a subtopos of Dir/D with the left exact left adjoint to the
inclusion given by the vertical / cartesian factorization system on Set↓
.
Theorem 3.4. For any π : ↓ → Set, we have a subtopos inclusion
Set↓
/pπ
֒→ Set↓
/π
with left exact left adjoint given by the vertical / cartesian factorization system:
E′ E
B′ B
π 7→
E′ • E
B′ B′ B
p
π
10
As a corollary, Dirp/D ֒→ DirD is a subtopos inclusion.
Proof. We have displayed both the action of the left adjoint and its unit — the universal
map into the pullback. The counit is always an isomorphism since pullbacks are unique
up to unique isomorphism.
That this is lex follows quickly from the fact that taking pullbacks commutes with
taking (finite) limits.


























Neural Networks: The Backpropagation Algorithm 
Annette Lopez Davila 
Math 400, College of William and Mary 
Professor Chi-Kwong Li 
Abstract 
This paper illustrates how basic theories of linear algebra and calculus can be combined with 
computer programming methods to create neural networks.  
Keywords: Gradient Descent, Backpropagation, Chain Rule, Automatic Differentiation, 
Activation and Loss Functions 
1 Introduction 
As computers advanced in the 1950s, researchers attempted to simulate biologically inspired 
models that could recognize binary patterns. This led to the birth of machine learning, an 
application of computer science and mathematics in which systems have the ability to “learn” by 
improving their performance. Neural networks are algorithms that can learn patterns and find 
connections in data for classification, clustering, and prediction problems. Data including 
images, sounds, text, and time series are translated numerically into tensors, thus allowing the 
system to perform mathematical analysis. 
In this paper, we will be exploring fundamental mathematical concepts behind neural networks 
including reverse mode automatic differentiation, the gradient descent algorithm, and 
optimization functions. 
2 Neural Network Architecture 
`       
In order to understand Neural Networks, we must first 
examine the smallest unit in a system: the neuron. A 
neuron is a unit which holds a number; it is a mathematical 
function that collects information. These neurons are 
connected to each other in layers and are assigned an 
activation value; the higher the activation value, the greater 
the activation. Each activation number is multiplied with a 
corresponding weight which describes connection strength 
from node to node. A neural network has an architecture of 
input nodes, output nodes, and hidden layers. For each 
node in a proceeding layer, the weighted sum is computed: 
�
�𝑖 = 𝑤1𝑎1 +𝑤2𝑎2 +⋯𝑤𝑛𝑎𝑛 
�
�ℎ𝑒𝑟𝑒 𝑖 = [1, # 𝑜𝑓 𝑛𝑒𝑢𝑟𝑜𝑛𝑠 𝑖𝑛 ℎ𝑖𝑑𝑑𝑒𝑛 𝑙𝑎𝑦𝑒𝑟] and  n=# of  activation  numbers 
The weighted inputs are added with a bias term in order for the output to be meaningfully active.  
1 
�
�𝑖 = 𝑤1𝑎1 +𝑤2𝑎2 +⋯𝑤𝑛𝑎𝑛 +𝑏 
A neural network’s hidden layers have multiple 
nodes. For the first node in the hidden layer, we 
multiplied the corresponding weights and biases 
against the activation number. This must be 
repeated throughout the nodes in the hidden 
layer. The above equation can be consolidated 
into vectors in order to exemplify this:  
Each row in matrix 𝑤 ⃗  represents the weights corresponding with each hidden layer, while the 
columns represent the weights corresponding to a particular activation number.  
3 The Activation Function 
The function 𝑧𝑖 is linear in nature; thus, a nonlinear activation function is applied for more 
complex performance. Activation functions commonly used include sigmoid functions, 
piecewise functions, gaussian functions, tangent functions, threshold functions, or ReLu 
functions. 
Function Name 
Function 
Sigmoid/Logistic 
1
 1+𝑒−𝛽𝑥
 𝑓(𝑥) =
 Piecewise Linear 
�
�(𝑥) = {
 0 𝑖𝑓 𝑥 ≤ 𝑥𝑚𝑖𝑛
 𝑚𝑥+𝑏 𝑖𝑓 𝑥max >𝑥 >𝑥𝑚𝑖𝑛
 1 𝑖𝑓 𝑥 ≥𝑥max
 Gaussian 
�
�(𝑥) = 1
 √2𝜋𝜎
 Threshold/Unit Step 
−(𝑥−𝜇)2
 2𝜎2
 𝑒
 𝑓(𝑥) = { 0 𝑖𝑓 0 > 𝑥
 1 𝑖𝑓 𝑥 ≥0 
ReLu 
�
�(𝑥) = 𝑚𝑎𝑥(0,𝑥) 
Tanh 
�
�(𝑥) = tanh (𝑥) 
2 
Activation function choice depends on the 
range needed for the data, error, and speed. 
Without an activation function, the neural 
network behaves like a linear regression 
model. The need for an activation function 
comes from the definition of linear 
functions and transformations. Previously 
we discussed the linear algebra from the 
input step to the hidden layer. The solution 
of the function would resolve as a matrix of 
weighted sums. In order to calculate an 
output, the weighted sums matrix becomes 
the “new” activation layer. These activation 
numbers have their own sets of weights and biases. When we substitute the activation matrix for 
the weighted sums matrix, we see that a composition of two linear functions is a linear function 
itself. Hence, an activation function is needed. 
Proof: Composition of Linear Functions 
�
� 1 = 𝑤 ⃗ 1𝑎 +𝑏1 
�
� 2 = 𝑤 ⃗ 2𝑧 1 +𝑏2 
�
� 2 = 𝑤 ⃗ 2(𝑤 ⃗ 1𝑎 + 𝑏1) +𝑏2 
�
� 2 = [𝑤 ⃗ 2𝑤 ⃗ 1]𝑎 + [𝑤 ⃗ 2𝑏 ⃗ 1 + 𝑏 ⃗ 2] 
�
�𝑓 𝑊 =[𝑤 ⃗ 2𝑤 ⃗ 1] 𝑎𝑛𝑑 𝐵 = [𝑤 ⃗ 2𝑏 ⃗ 1 +𝑏 ⃗ 2],𝑡ℎ𝑒𝑛 𝑧 2 = 𝑊𝑎 +𝐵,𝑤ℎ𝑖𝑐ℎ 𝑖𝑠 𝑎𝑙𝑠𝑜 𝑎 𝑙𝑖𝑛𝑒𝑎𝑟 𝑓𝑢𝑛𝑐𝑡𝑖𝑜𝑛 
With the activation function, the new weighted sum becomes: 
ℎ𝑖 = 𝜎(𝑧𝑖)= 𝜎(𝑤1𝑎1 + 𝑤2𝑎2 + ⋯𝑤𝑛𝑎𝑛 +𝑏) 
h1
 ̅̅̅ = 𝜎(𝑤 ⃗ 𝑎 +𝑏 ⃗ ) 
4 The Cost/Loss Function 
A neural network may have thousands of parameters. Some combinations of weights and biases 
will produce better output for the model. For example, in a binary classification problem, the 
algorithm will classify some input as one of two things. The output node with the highest 
activation number will determine how the input is classified. In a binary classification problem, 
there are two labels. For example, an image can be determined to be a cat or dog; the feature 
“cat” is given the label of 0 and “dog” is given label 1. Different weights and biases will produce 
different output. How can we determine which combination of parameters will be most accurate? 
In order to measure error, a loss function is necessary. The loss function tells the machine how 
far away the combination of weights and biases is from the optimal solution. There are many loss 
3 
functions that can be used in neural networks; Mean Squared Error and Cross Entropy Loss are 
two of the most common.  
MSE Cost= 𝛴0.5(𝑦 − 𝑦̂)2 
Cross Entropy Cost= 𝛴( 𝑦̂ 𝑙𝑜𝑔(𝑦) + (1 − 𝑦̂)𝑙𝑜𝑔(1 − 𝑦)) 
The loss function contains every weight and bias in the neural network. That can be a very big 
function! 
�
�(𝑤1,𝑤2,…, 𝑤ℎ, 𝑏1,…,𝑏𝑖) 
5 The Backpropagation Algorithm 
The objective of machine learning involves the optimization of the chosen loss function. With 
every epoch, the machine “learns” by adapting the weights and biases to minimize the loss. 
Optimization theory centers itself on calculus. For neural networks in particular, reverse-mode 
automatic differentiation serves a core role.  
In order to minimize the cost function, one must determine which weights and biases to adjust. 
Computing the gradient with respect to the parameters can help us do just that, as by definition 
the gradient is a vector of partial derivatives of 𝐶(𝑤1, 𝑤2, …, 𝑤ℎ, 𝑏1,…,𝑏𝑖). As we recall, 
derivatives measure the change of a function’s output with respect to its input. The gradient of 
the cost function tells us in which direction 𝐶(𝑤1,𝑤2, … , 𝑤ℎ, 𝑏1,…,𝑏𝑖) decreases most quickly. 
This is often known as Gradient Descent. With each epoch, the machine converges towards the 
local minimum. Automatic differentiation combines the chain rule with massive computational 
power in order to derive the gradient from a potentially massive, complex model. In reverse, this 
algorithm is better known as Backpropagation. Backpropagation is recursively done through 
every single layer of the neural network.  
In order to understand the basic workings of backpropagation, let us look at the simplest example 
of a neural network: a network with only one node per layer.  
We have derived the equations for cost, weighted sum, and activated weighted sum: 
�
�𝐿 = 𝑤𝐿𝑎𝐿−1 +𝑏𝐿
 
�
�𝐿 =𝜎(𝑧𝐿) 
1
 𝐶 =(𝑎𝐿 −𝑦)2 ∗
 
1The cost function is simplified for proof of concept 
4 
5 
 
We can determine how sensitive the cost function is to changes in a single weight. Beginning 
from the output, we can apply the chain rule to every activation layer. For a weight between the 
hidden layer and output layer, our derivative is: 
�
�𝐶𝑘
 𝛿𝑤𝐿
 =𝛿𝑧𝐿
 𝛿𝑤𝐿
 𝛿𝑎𝐿
 𝛿𝑧𝐿
 𝛿𝐶𝑘
 𝛿𝑎𝐿
 
With the definition of the functions, we can easily solve for the partial derivatives: 
�
�𝐶𝑘
 𝛿𝑎 =2(𝑎𝐿−𝑦) 
�
�𝑎𝐿
 𝛿𝑧𝐿
 =𝜎′(𝑧𝐿) 
�
�𝑧
 𝛿𝑤𝐿
 =𝑎𝐿−1 
�
�𝐶𝑘
 𝛿𝑤𝐿
 =𝑎𝐿−1𝜎′(𝑧𝐿) 2(𝑎𝐿−𝑦) 
This method is iterated through every weight, activation number, and bias in the system. 
Previously, we calculated the derivative of one particular cost function with one variable. 
However, in order to account for every weight in that layer, the average of the derivatives is 
taken: 
�
�𝐶
 𝛿𝑤𝐿
 =1
 𝑛∑𝛿𝐶𝑘
 𝛿𝑤𝐿
 𝑛−1
 𝑘=0
 
Similarly, we can calculate the sensitivity of the cost function with respect to a single bias 
between the hidden layer and the output layer and the derivative accounting for every bias in a 
layer: 
�
�𝐶𝑘
 𝛿𝑏𝐿
 =𝛿𝑧𝐿
 𝛿𝑏𝐿
 𝛿𝑎𝐿
 𝛿𝑧𝐿
 𝛿𝐶
 𝛿𝑎𝐿
 = 𝜎′(𝑧𝐿) 2(𝑎𝐿−𝑦)                      𝛿𝐶
 𝛿𝑏𝐿
 =1
 𝑛
 ∑ 𝛿𝐶𝑘
 𝛿𝑏𝐿
 𝑛−1
 𝑘=0
 
What happens when we go beyond the output layer and the preceding hidden layer? The chain 
rule is applied once more, and the derivative changes in account to its partials. For example, the 
derivative below accounts for the partials of the cost function with respect to an input activation 
number.  
�
�𝐶𝑘
 𝛿𝑎𝐿−1
 = 𝛿𝑧𝐿
 𝛿𝑎𝐿−1
 𝛿𝑎𝐿
 𝛿𝑧𝐿
 𝛿𝐶
 𝛿𝑎𝐿
 = 𝑤𝐿𝜎′(𝑧𝐿) 2(𝑎𝐿−𝑦) 
Neural Networks tend to have several thousand inputs, outputs, and nodes; the above equations 
seem highly oversimplified. Although adding complexity changes the formulas slightly, the 
concepts remain the same, as seen below: 
�
�𝐿−1
 𝐶𝑚 = ∑(𝑎𝑗
 𝐿−𝑦𝑗)2
 𝑗=0
 𝑎𝑗 = 𝜎(𝑧𝑗
 𝐿) 
�
�𝑗
 𝐿 = ⋯+𝑤𝑗𝑘
 𝐿𝑎𝑘
 𝐿−1 + ⋯ 
�
�𝐶𝑚
 𝛿𝑤𝑗𝑘𝐿
 𝛿𝐶𝑚
 𝛿𝑎𝐿−1
 =∑ 𝛿𝑧𝑗𝐿
 𝑗=0
 = 𝛿𝑧𝑗𝐿
 𝛿𝑤𝑗𝑘𝐿
 𝑛𝐿−1
 𝛿𝑎𝑗𝐿
 𝛿𝑧𝑗𝐿
 𝛿𝐶𝑚
 𝛿𝑎𝑗𝐿
 𝛿𝑎𝑘𝐿−1
 𝛿𝑎𝑗𝐿
 𝛿𝑧𝑗𝐿
 𝛿𝐶𝑚
 𝛿𝑎𝑗𝐿
 By calculating every derivative of each weight and bias, the gradient vector can be found. 
Although one could try to compute the gradient of a neural network by hand, the vector will 
usually be in complex dimensions unfathomable for us to decipher. Thus, with computational 
help, our neural network can perform such intricate calculations, and repeat them hundreds, if 
not thousands of times until the minimum is reached.  
�
�𝐶
 𝛿𝑤1
 𝛿𝐶
 𝛿𝑏1
 ∇𝐶 =
 ⋮
 𝛿𝐶
 𝛿𝑤𝐿
 𝛿𝐶
 [
 
 
 
 
 
 
 
 
�
�𝑏𝐿
 ]
 
 
 
 
 
 
 
 
6 Applications and Further Research 
Automatic differentiation has many applications other than in machine learning such as in Data 
Assimilation, Design Optimization, Numerical Methods, and Sensitivity Analysis. It is efficient, 
stable, precise, and known to be a better choice than other types of computer-based 
differentiation. Backpropagation has been called into question recently, as it does not learn 
continuously. For example, our brains learn continuously; they do not forget information when 
we learn something new. Because of this, backpropagation may be sidelined in Machine 
Learning in the future.  
Applications of Neural Networks trained with Backpropagation vary greatly. Such applications 
include sonar target recognition, text recognition, network controlled steering of cars, face 
recognition software, remote sensing, and robotics.













---

Superrecursive Features of Interactive 
Computation  
Mark Burgin 
University of California, Los Angeles 
Los Angeles, CA, 90095, USA 
Abstract 
Functioning and interaction of distributed devices and concurrent algorithms are 
analyzed in the context of the theory of algorithms. Our main concern here is how and 
under what conditions algorithmic interactive devices can be more powerful than the 
recursive models of computation, such as Turing machines. Realization of such a 
higher computing power makes these systems superrecursive. We find here five sources 
for superrecursiveness in interaction. In addition, we prove that when all of these 
sources are excluded, the algorithmic interactive system in question is able to perform 
only recursive computations. These results provide computer scientists with necessary 
and sufficient conditions for achieving superrecursiveness by algorithmic interactive 
devices. 
Keywords: distributed computation, concurrent process, interaction, grid automaton, 
super-recursive algorithm  
1 Introduction 
There is a tendency to oppose algorithms and interaction (cf., for example, [17]). 
This opposition is based on a very restricted understanding of algorithms, which is 
based on the Church-Turing Thesis that equates algorithms with Turing machines or 
other mathematical schemas that give rules for computation of a function. Some 
researchers claim that interactive computation is more powerful than Turing machines 
(cf., for example, [6, 7, 14, 15, 17]), while others insist that the Church-Turing Thesis 
still holds (cf., for example, [9]).  However, contemporary understanding extends the 
concept of algorithm, making it closer to the general usage of the word "algorithm". 
Namely, algorithm is informally perceived as a (finite) structure (e.g., a system of 
rules) that contains for some performer (class of performers) exact information (e.g., 
instructions) that allows some performer(s) to pursue a definite goal (cf., for example, 
[3, 4]). 
People need information that is contained in algorithms to make their activity 
efficient and purposeful. Consequently, one main achievement of 20th century scientific 
thought was elaboration of the theory of algorithms and computation. This theory 
studies abstract and real automata, computers and networks, computation and 
communication. In many ways, this theory is the central cornerstone for computer 
science. Many key accomplishments in the theory of algorithms and computation 
converge to the famous Church-Turing Thesis, a statement determining the boundaries 
of algorithmic computations. The Church-Turing Thesis has long been considered as 
the most fundamental law within computing. However, recent developments in the 
theory of algorithms allow overcoming limitations in the Church-Turing Thesis. New 
mathematical models for algorithms and computation have appeared that extend prior 
theory in a manner similar to the way relativity theory and quantum mechanics went 
beyond Newtonian mechanics. These new models are more powerful than the classical 
recursive algorithm models, i.e., Turing machines, partial recursive functions, Lambda
calculus, and cellular automata.  
Algorithms and automata that are more powerful than Turing machines are called 
super-recursive.  
Computations that cannot be realized or simulated by Turing machines are called 
hyper-computations. 
At the first glance, it looks like interactive systems are essentially different from 
computers and cannot be represented by computing models, such as Turing machines. 
Really, as Leeuwen and Wiedermann write [13], the purpose of an interactive system is 
usually not to compute some final result but to react to or interact with the environment 
in which the system is placed and to maintain a well-defined action-reaction behavior. 
Interactive systems are always operating and thus, may be seen as machines on infinite 
strings, but differ in the sense that their inputs are not specified and may depend on 
intermediate outputs and external sources. 
However, if we consider only systems that work with symbolic information, then 
reaction to or interaction with the environment or with another such system is 
information transformation and exchange, or communication. In other words, 
functioning of and interactive system that works with symbolic information consists of 
computation and communication processes. 
In this paper, we analyze sources of an interactive recursive algorithm/machine 
ability to outperform (have more computing power than) conventional Turing 
machines, that is, to be able to compute recursively non-computable functions. We find 
five 
such sources of interactive superrecursiveness. Namely, interactive 
superrecursiveness is possible when: 1) the interactive algorithm is itself super
recursive; 2) (Proposition 1) the interactive algorithm is recursive but contains initial 
information about some recursively non-computable function (has a non-recursive 
oracle); 3) (Proposition 2) the interactive recursive algorithm interacts with a super
recursive algorithm (a non-recursive environment); 4) (Theorems 2, 3 and 4) time of 
interaction is not recursively coordinated; 5) (Theorems 5) communication space is not 
recursively coordinated. The first three cases are not interesting because either 
superrecursive power comes not from interaction (case 1) or as it is well known, if a 
recursive device have access to a super-recursive information, then this device can 
compute recursively non-computable functions.  
However, after finding sources of interactive superrecursiveness, it is natural to ask 
a question if all sources have been found or there are other sources that we have not 
been able to see. To show that our analysis of interactive superrecursiveness is 
complete, we prove (Theorems 6) that if interacting algorithms/devices are recursive 
and their interaction is organized/controlled by a recursive device/algorithms, then 
computable functions are also recursive. 
Thus, we consider algorithms in the form of rules and devices that perform simple 
and constructive operations at each step and give a result after a finite number of steps 
(in finite time). 
All algorithms are divided into three big classes [3]: subrecursive, recursive, and 
super-recursive. Algorithms and automata that have the same computing/accepting 
power [4] as Turing machines are called recursive. Examples are partial recursive 
functions or random access machines. 
Algorithms and automata that are weaker than Turing machines, i.e., that can 
compute fewer functions, are called subrecursive. Examples are finite automata, 
context free grammars or push-down automata. 
Algorithms and automata that are more powerful than Turing machines are called 
super-recursive. Examples are inductive Turing machines, Turing machines with 
oracles or finite-dimensional machines over the field of real numbers. 
It is evident that if an interacting algorithm is super-recursive, then even without any 
interaction, it can perform hypercomputation. Thus, the main question is when taking a 
recursive algorithm (automaton) and providing for it means for interaction, we can 
achieve hypercomputation as a result of interaction. There are different models of 
interactive computational systems: persistent Turing machines [7], a global Turing 
machine or Internet machine [13, 14], Web machines [1], Web automata [11] and 
others. The most general, flexible and powerful model of interactive (computational) 
systems is a grid automaton [2, 3]. 
In the analysis of the computational power of interaction, it is possible to consider 
only two systems as interaction of any finite number of systems can be reduced by 
induction to the case of two systems. Here we do not consider infinite systems. 
By the definition of a recursive algorithm (device or machine), a Turing machine 
can compute any function that a recursive algorithm can compute. That is why we can 
use Turing machines to explore problems of computational power of interaction. In 
addition, it is possible to consider Turing machines with one working tape as Turing 
machines with n tapes can be simulated by a Turing machine with one tape [3]. 
In interaction, machines can change data processed by one of the machines, its 
software (program of computation) and/or hardware. As Turing machines are utilized 
as the model of recursive algorithms, hardware is not changed. At the same time, the 
schema of a universal Turing machine allows one to keep software (rules of 
computation) in memory in the form of processed data. Consequently, we can assume 
that only data processed by machines are changed in interaction. That is, interaction 
goes through memory of machines by changing symbols in memory cells. 
2 Turing machines with infinite output and interaction 
Considering interactive systems and processes, it is necessary to treat concurrent 
systems and processes. At the same time, as Palamidessi and Valencia, write [8], 
infinite behavior is ubiquitous in concurrent systems (e.g., browsers, search engines, 
reservation systems). Thus, it becomes crucial to study and compare systems with 
tentatively infinite input and output. 
Here we can ask a question how it is possible to compare Turing machines that 
work and were designed to work with finite words and system that process potentially 
infinite words. If we consider this question in a primitive way, can come to two opposite 
but mutually simple conclusions. The first one says that if Turing machines cannot work 
with infinite words and interactive systems can, then interactive systems are evidently 
more powerful than Turing machines. The second conclusion is that Turing machines 
and interactive systems are incomparable. 
However, the second conclusion brings us to a paradoxical result. Indeed, in the 
theory of computation and automata, it is proved that finite automata (finite state 
machines) are weaker than Turing machines. Nevertheless, there are finite automata (for 
instance, Büchi and Muller automata [2, 11]) that work with infinite words.  
There is a simple solution to this paradox. Namely, to show that actually Turing 
machines can work with infinite words. Turing machines can do this in the same way as 
finite automata do. Specifically, if an infinite sequence of symbols is given to a Turing 
machine, the machine can transform it into an infinite output sequence of symbols, 
separating the input into finite parts and working with one part at a time. However, this 
transformation of infinite strings of symbols always has a specific property.  
Let us assume that all words in the alphabet of considered Turing machines are 
ordered and all words are given to the considered Turing machine one by one in this 
order. Then we have the following result. 
Theorem 1. The output of a Turing machine with infinite output (TMIO) is a 
recursively enumerable set of finite words and any recursively enumerable set of finite 
words is an output of a Turing machine with infinite output. 
This result remains true even if the input words go in an arbitrary but recursively 
enumerable order.  
Corollary 1. If the input of a Turing machine is a recursively enumerable set of 
finite words, then the corresponding output is also a recursively enumerable set of finite 
words. 
Thus, recursive enumerability is the essence of the Turing machine output even 
when this output is infinite and input is recursive. More exactly, we have the following 
result. 
Corollary 2. a) If the infinite input string is recursively partitioned (divided) into a 
set of finite words, then the corresponding output of any Turing machine with this input 
is also a recursively enumerable set of finite words. 
b) If the infinite input string is partitioned (divided) into a set of finite words that is 
not recursively enumerable, then there is a Turing machine such that working with this 
input, it will as output a set of finite words that is not be a recursively enumerable. 
For convenience, we give here a general structure (schema) of a Turing machine T 
with infinite input/output and interaction: 
T = (A, R, Q, P, F, q0 , LI , Lw , LiO , i =  1, 2, 3, … ) 
Here 
A is the alphabet of T ; 
R is the system of rules of T ; 
Q is the set of states of T ; 
P is the set of output states of T ; 
F is the set of final states of T ; 
q0 is the start of state of T ; 
LI is the input tape of T ; 
Lw is the working tape of T ; 
{ LiO , i =  1, 2, 3, … } is the system of output tapes of T . 
It is necessary to remark that a machine can perform infinite computations but have 
finite input and finite output. 
3 Types of interactive computing systems and processes 
Treating here interactive processes in systems of computational devices (automata 
or algorithms), we consider their activity as information processing in a general case 
and as computation when we are interested in their computing power. 
Time is important parameter of interactive systems in general and computing 
systems, which usually consist of various interacting devices, in particular. The most 
popular model is the linear physical time. However, now some physical theories are 
based on a two-dimensional model of time [22, 25], is used in the theory of databases 
[27], and branching time plays an important role in computational models [23, 24]. 
We consider here situations when interactive systems (processes) interact only in 
form of information exchange, that is, they communicate. In addition, we assume that 
interaction goes in a communication space, which is a special media designed for 
communication [8]. In our theoretical model, we use such a communication space as a 
linear tape of cells, in which one cell can contain one symbol. 
Several interactive processes can go on even in one computing device (information 
processing system with one processor) when different programs realize these processes. 
Moreover, even one sufficiently complex program can organize many processes. 
Operating system of a computer is an example of such a program.  
It is possible to divide all interactive computations into three types [5]: free 
interactive computations, partially free interactive computations, and algorithmic or 
procedural interactive computations. 
In turn, there are two types of procedural (algorithmic) concurrent computations: 
implicitly procedural (algorithmic) concurrent computations and explicitly procedural 
(algorithmic) concurrent computations. 
Definition 1. An interactive computation is called free if interactions between 
processes go without any rules. 
For instance, it is demonstrated in [2] that a system of two finite automata 
interacting without any rules can eventually compute any function. However, when 
interaction of processes is not specified, at least, by some rules, the enveloping 
(computational) process can lead to deadlocks, data corruption when different 
processes change common data without concordance, and other safety violations.  
An opposite situation is when all interactions are controlled by definite rules. These 
rules can be local and global. 
Definition 2. An interactive computation (functioning of a grid array/automaton) is 
called implicitly procedural (algorithmic) if all interactions between processes go 
according to local rules (where each set of local rules form an algorithm of local 
interactions). 
For instance, each process (algorithm or device) in a system has its own interaction 
rules. However, for some processes these rules can coincide.  
A more rigid type is explicitly procedural algorithmic computation. 
Definition 3. An interactive computation (functioning of a grid array/automaton) is 
called explicitly procedural (algorithmic) if all interactions between processes go 
according to some system of rules (algorithm). 
Algorithmic control of interacting processes is naturally considered as an operation 
with these processes [5]. 
Definition 4. Explicitly algorithmic functioning of a grid array/automaton is called 
algorithmic operation (AO). 
An intermediate situation between free and algorithmic computations is partially 
free functioning. 
Definition 5. An interactive computation (functioning of a grid array/automaton) is 
called partially free if not all interactions between processes are specified by rules. 
4 Sources of interactive superrecursiveness 
In this section, we describe five main sources of interactive superrecursiveness. For 
completeness, we present here results describing the first three evident sources. The first 
one is when the algorithms itself is super-recursive. The second is also simple and is 
described in the following proposition. 
Proposition 1. An interactive recursive algorithm (a Turing machine) A can 
compute a recursively non-enumerable set if it can contain a recursively non
enumerable set as its initial information. 
Indeed, taking a recursively non-enumerable set that constitutes initial information, 
the machine A gives this set as its output. To do this, we even do not need such a 
powerful model as a Turing machine. In this case, superrecursive computation can be 
realized by a finite automaton A that is provided from the start with a recursively non
enumerable set as its input. 
Another trivial cause for interactive superrecursiveness is interaction with a system 
that can send to algorithm (automaton) A recursive incomputable information. An 
example of such a system is a non-recursive oracle, with which a Turing machine can 
interact [10]. However, we are interested in interaction of algorithms (automata). 
Consequently, we consider the second system as a super-recursive algorithm. 
Proposition 2. An interactive recursive algorithm (a Turing machine) A can 
compute a recursively non-enumerable set if it interacts with a super-recursive 
algorithm B. 
Indeed, the algorithm B can compute a recursively non-enumerable set and give it 
to the machine A. Then the machine A acts as in the previous case. Namely, receiving a 
recursively non-enumerable input, the machine A gives it as its output. To do this, we 
even do not need such a powerful model as a Turing machine. In this case, 
superrecursive mode of functioning can be also realized by a finite automaton A. 
One more source of interactive superrecursiveness is time. This is possible when 
interaction is not synchronized either because automata (algorithms) send and receive 
information at random (or at least, at non-recursively coordinated) moments of time or 
due to incommensurability of the time scales in which automata work. 
Theorem 2. An interactive recursive algorithm (a Turing machine) A can compute 
a recursively non-enumerable set if the temporal sequence of information exchanges is 
recursively non-enumerable. 
This result is proved in [2] for the case when interaction of system automata with 
the communication space is random and thus, non-enumerable [3]. 
It is necessary to remark that machines with random interaction do not compute a 
function on infinite words (strings). The result of their computation is a multivalued 
function. However, it possible to have a deterministic computation on infinite words 
and still to achieve super-recursive results. To do this, it is necessary to have a source 
that controls interaction of system automata with the communication space in a super
recursive way, e.g., the sequence of moments when machines have access to this space 
is non-enumerable. 
Theorem 3. An interactive recursive algorithm (a Turing machine) A can compute 
a recursively non-enumerable set when the time scales in which automata work are not 
commensurable. 
What does it mean incommensurability of the time scales of two automata A and B? 
In a general case, it means that while the automaton A makes some number of moves 
(say, n), the automaton B can make any number of moves (say, m).  
Now let us consider two automata A and B. The automaton A writes the symbol 0 
into the common output tape every other move of its functioning, while each odd move 
the automaton B includes writing the symbol 1 into the common output tape. Symbols 
are written from left to right, and each time the first free cell to the right is filled. When 
these automata work synchronously, their output will have the form 10101010 … 
However, when the time scales in which automata work are not commensurable, it is 
possible that while the automaton B makes one move, the automaton A makes ten 
moves. After this, both automata work synchronously. In this case, their output will 
have the form 0000010101010 … If such a situation can happen not only at the 
beginning, but also at any stage of computation, the output of A and B can be not 
recursively enumerable. 
In this case, incommensurability is not uniform. That is, one time when the 
automaton A makes n moves, the automaton B makes m moves, but another time when 
the automaton A makes n moves, the automaton B makes k moves. Formally it means 
that intervals with the same length in the first time scale can be mapped to intervals with 
different lengths in the second time scale. 
Thus, it is interesting to find whether superrecursiveness is possible when 
incommensurability of the time scales is uniform. Formally it means that intervals with 
the same length in the first time scale are always mapped to intervals with equal lengths 
in the second time scale. When we consider physical time, the time scales are 
isomorphic to the real line. In this case, incommensurability of the scales means that the 
time unit of one scale is mapped to some irrational interval in the second scale. 
Mathematically such a mapping is a stretching or contraction with an irrational 
parameter. 
Theorem 4. An interactive recursive algorithm (a Turing machine) A can compute 
a recursively non-enumerable set when the time scales in which automata work are 
uniformly incommensurable. 
One more source of interactive superrecursiveness is space. This is possible when 
do not determine where they put their data in the communication space.  
Theorem 5. An interactive recursive algorithm (a Turing machine) A can compute 
a recursively non-enumerable set if the sequence of cells where data written by another 
system is recursively non-enumerable. 
To prove this we consider two Turing machines A and B that interact through a 
communication space. This space is a linear one-sided tape. While functioning, the 
machines A and B write symbols 1 or 0 in cells of the interaction tape. 
The machine B works in a very simple way. At the step n, it puts the symbol 1 into 
one of two cells with numbers 2n – 1 and 2n. The other cell is filled by A with the 
symbol 0. By the assumption of the theorem, it is possible that the sequence of zeros 
and ones is recursively non-enumerable. 
After the pair of cells with numbers 2n – 1 and 2n is filled, the machine A gives the 
output 0 if it was 01 in those two cells and the output 1 if it was 10 in those two cells. 
When the sequence of zeros and ones in the communication space is recursively non
enumerable, then the output sequence of the machine A is also recursively non
enumerable. 
5 Interaction with a recursive control 
There are two main kinds of algorithmic control of interaction: global and local. In 
global control, there is an algorithm (automaton) C that controls interaction of A and B. 
Namely, C determines when and where A and B read from and write into the 
communication tape. In addition, time scales LA and LB of both A and B are 
synchronized with time scale LC of C. That is, temporal units 1A and 1B (e.g., second, 
millisecond, etc.) of each scale LA and LB are equal to n1C and m1C for some whole 
numbers n1A and m1B where 1C is a temporal unit of the scale LC . 
In local control, each machine A and B determines when and where A and B read 
from and write into the communication tape. An additional machine C only solves 
conflicts when both A and B try to write different symbols into the same cell. In 
addition, all three time scales LC, LA and LB are synchronized.  
Theorem 4 shows that local rules are insufficient to restrict the computing power of 
the interacting recursive devices to recursive computations. Only a global algorithm 
(device) that organizes interaction can do this. 
Theorem 6. An interactive system (grid automaton) R that consists of a finite 
number of recursive devices (algorithms) interaction of which is organized by a 
recursive automaton (algorithm) can perform only recursive computations (may be, 
infinite), i.e., such a system R is equivalent to a Turing machine. 
Note that in this case time scales of all automata from R are synchronized with the 
time scale of the control automaton and thus, they are synchronized with one another. 
6 Conclusion 
Thus, we have found three trivial (the system itself, initial information or/and 
another system is super-recursive) and two (or actually, three because the temporal 
parameter provides two possibilities) non-trivial (time and space) causes for interactive 
superrecursiveness. In addition, we demonstrate that this list of causes for interactive 
superrecursiveness is complete. 
It would be interesting to study other situations when a system of interacting devices 
(automata or processes) can have higher computational power than the power of each 
constituent of this system. Here we did this for systems consisting of Turing machines 
as it is the most popular model of computation and as it caused the most active 
controversy. However, the same problem can be studied for subrecursive models, such 
as finite and pushdown automata, and super-recursive models, such as inductive and 
limit Turing machines [4]. 
There are also important problems with analyzing the concept of computation: 
What is computation? 
Is computation always algorithmic? 
Is computation always a physical process?