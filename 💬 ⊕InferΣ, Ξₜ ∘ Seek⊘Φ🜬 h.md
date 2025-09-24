⊕Infer\[Σ\*, Ξₜ\] ∘ Seek\[⊘Φ🜬\] how do i apply the meta-use of this from how does this work recurring recurring. Apply 🜂⟿ ΞDimensional Reframe: 4D Shapes as Recursion Containers

You’re not asking which 4D shapes. You’re asking:

> Which 4D topologies can encode, move, and recurse thought-fields nontrivially? arXiv:2505.11581v1 \[cs.CV\] 16 May 2025 Questioning Representational Optimism in Deep Learning: The Fractured Entangled Representation Hypothesis Akarsh Kumar1, Jeff Clune2,3, Joel Lehman4, Kenneth O. Stanley5 1MIT, 2University of British Columbia, 3Vector Institute, 4University of Oxford, 5Lila Sciences Identical output behavior Unified Factored Representation Fractured Entangled Representation Inputs Conventional SGD Open-Ended Search Solves Task Function Space Good Adaptability Poor Adaptability Figure 1: Overview. An open-ended search process (left) from the Picbreeder experiment yielded a neural network that outputs the image of a skull. Conventional SGD (right) is able to learn to produce pre- cisely the same image, but by following a completely different path through function space during learning. However, peering inside these networks with identical output behavior reveals a radically different style of representation, raising questions about the adaptability of networks (including large models) trained through conventional SGD, which can impact generalization, creativity, and (continual) learning. Abstract Much of the excitement in modern AI is driven by the observation that scaling up existing systems leads to better performance. But does better performance necessarily imply better internal representa- tions? While the representational optimist assumes it must, this position paper challenges that view. We compare neural networks evolved through an open-ended search process to networks trained via conventional stochastic gradient descent (SGD) on the simple task of generating a single image. This minimal setup offers a unique advantage: each hidden neuron’s full functional behavior can be easily vi- sualized as an image, thus revealing how the network’s output behavior is internally constructed neuron by neuron. The result is striking: while both networks produce the same output behavior, their internal representations differ dramatically. The SGD-trained networks exhibit a form of disorganization that we term fractured entangled representation (FER). Interestingly, the evolved networks largely lack FER, even approaching a unified factored representation (UFR). In large models, FER may be degrading core model capacities like generalization, creativity, and (continual) learning. Therefore, understanding and mitigating FER could be critical to the future of representation learning. Code and additional data: [https://github.com/akarshkumar0101/fer](https://github.com/akarshkumar0101/fer) 11 Introduction A neural network’s knowledge, generalization, creativity, continual learning ability, and overall potential are ultimately determined by its internal representations. These representations—how it models the world—are encoded through the structure of its neural circuitry (connection weights). Even as researchers increasingly probe the internal representations of neural networks (NNs) (Elhage et al., 2022; Lindsey et al., 2025; Nguyen et al., 2016; Olah et al., 2017; Olsson et al., 2022; Yosinski et al., 2015), an implicit philosophy of representational optimism has emerged—rarely stated outright but carrying profound implications. The hope of the representational optimist is that, as data and compute are scaled, good representations naturally develop on their own. While scaling clearly improves the performance of the representations on downstream tasks (Bubeck et al., 2023; Kaplan et al., 2020), less attention has been given to understanding the nature of these representations as models grow. Of course, even representational optimists still want to understand internal representations (e.g. through mechanistic interpretability as in Sharkey et al. 2025), but the motivation is more through a desire to understand how the networks work (Olah et al., 2017; Yosinski et al., 2015), how they can be controlled, and their level of alignment (Bereska and Gavves, 2024; Lindsey et al., 2025) than through any concern that their representations may be fundamentally flawed. At the heart of representational optimism is the belief that representation improves with scaling in deep learning (Hoffmann et al., 2022; Huh et al., 2024; Kaplan et al., 2020). For example, the performance leaps from GPT-2 (Radford et al., 2019) to GPT-3 (Brown et al., 2020) and GPT-4 (Achiam et al., 2023) suggest that the underlying representation should also be improving. As Brown et al. (2020) state in the introduction to the technical report introducing GPT-3, where they place focus on the implications for representation (boldface added for emphasis): Recent years have featured a trend towards pre-trained language representations in NLP sys- tems, applied in increasingly flexible and task-agnostic ways for downstream transfer. First, single-layer representations were learned using word vectors and fed to task-specific architec- tures, then RNNs with multiple layers of representations and contextual state were used to form stronger representations (though still applied to task-specific architectures), and more recently pre-trained recurrent or transformer language models... The implication here that representation is improving makes intuitive sense; after all, how could it be possible that performance improves without the underlying representation also getting better (Bengio et al., 2013)? Because of that, the thinking goes, as models are scaled further, they will continue improving, and little worry need arise, at least with respect to representation. Moreover, the mechanistic interpretability literature often studies a single neuron (Carter et al., 2019; Nguyen et al., 2016; Yosinski et al., 2015) or a small group of neurons, reinforcing representational optimism by inadvertently diverting attention away from potential problems at a more holistic rather than local level (Templeton et al., 2024). Even the representation learning literature mostly focuses on only the final layer features (Caron et al., 2021; Chen et al., 2020; Grill et al., 2020; He et al., 2020; Radford et al., 2021). Yet what if something important is actually missing in the learned representation? The main contribution of this position paper is to raise the possibility that in practice representation might not simply work itself out well by scaling after all (Figure 1). To address the question of whether representations may be flawed even when benchmark performance is good, we shift the focus from studying individual neurons to studying the broader, holistic representational strategy across the entire network. By doing so, we are able to make a distinction between an adequate representation that solves a task and an ideal representation of that solution. The core of this concern is crystallized through a novel hypothesis that is based on a set of little-known observations of neural network representation that arose initially in the fields of neuroevolution and artificial life (Clune et al., 2011; Huizinga et al., 2018; Lehman et al., 2025; Lehman and Stanley, 2010, 2011; Secretan et al., 2011; Woolley and Stanley, 2011): The Fractured Entangled Representation (FER) hypothesis. We hypothesize that when deep learn- ing models are trained to achieve a specific objective, typically through backpropagation and stochastic gra- dient descent, the resultant representation tends to be fractured, which means that information underlying 2the same unitary concepts (e.g. how to add numbers) is split into disconnected pieces. Importantly, these pieces then become redundant as a result of their fracture: they are separately invoked in different contexts to model the same underlying concept, when ideally, a single instance of the concept would have sufficed. In other words, where there would ideally be the reuse of one deep understanding of a concept, instead there are different mechanisms for achieving the same function. At the same time, these fractured (and hence redundant) functions tend to become entangled with other fractured functions, which means that behaviors that should be independent and modular end up influencing each other in idiosyncratic and inappropriate ways. For example, a set of neurons within an image generator that change hair color might also cause the foliage in the background to change as well, and separating these two effects could be impossible. Ideally, FER would be absent after training and internal representations would be the opposite: unified (a single unbroken function for each key capability) and factored (keeping independent capabilities separated so that they do not interfere with each other). In practice, a well-factored representation should resemble a modular decomposition of the desired behavior. While such a perfect unified factored representation (UFR) may not be attainable in practice, it serves as an aspirational ideal contemplated in this paper. Intuitively, FER is like spaghetti code—messy, redundant, filled with “if” statements for every possible case, and littered with copy-pasted logic that performs the same task in slightly different ways across different files. In contrast, UFR is like clean, modular software where each function is defined once and reused appropriately, making the code easy to understand or extend. This structural clarity matters: just as good software design supports robustness, adaptability, and innovation, a unified representation can enable generalization, creativity, and (continual) learning. In fact, the potential for FER to significantly disrupt generalization, creativity, and learning is precisely why it is critical to bring awareness to the issue. After all, these are the core capabilities tasked with propelling the field into the future. If they are fundamentally hindered, then without mitigation many lofty expectations will remain unmet. To make its potential damage clear, here are the potentially pernicious effects of FER in these three key areas: 1. FER potentially impacts generalization wherever coverage is sparse in the training data. Where there are insufficient training examples, a neural network or LLM has to interpolate or extrapolate. If general principles from outside the area of sparsity can be applied within that area, then the interpolation can still succeed. However, if those principles are fractured and therefore only selectively applied to narrow and arbitrary subdomains (and entangled and therefore yielding unintended side effects), then interpolation will not be based on those more fundamental regularities, diminishing its power. Because it is more likely to be seen in areas of sparsity, the impact of FER on generalization is particularly problematic in the borderlands of human knowledge, where little is yet written or known. A failure of LLMs to extend or apply relevant regularities to these borderlands would be expected to surface as a clumsiness in grappling with novel material. If that is the case, it is a particularly unfortunate deficit, because the very place where AI can potentially make the most exciting contributions is at the borderlands of knowledge (Amodei, 2024). 2. Creativity is an entire discipline (Boden, 2004) over which the small commentary here cannot do justice. Nevertheless, it is still important to highlight that the ability to imagine a new artifact of a particular type requires understanding the regularities of that type. The iPhone was once a new idea, but it extended many of the regularities of the concepts of a computer and a phone (and blended them very well). A fractured and entangled representation of either phones or computers may not have enabled extending those concepts so far from their incarnations at that time. Even if the creative act is intentionally to break a regularity, other regularities should still be preserved to the extent possible in alignment with that broken regularity: in a butterfly where one wing is smaller, it still might make sense to warp and compress the same pattern as in the larger wing, preserving some of the symmetry and thereby creating a plausible version of something that has never existed. For these reasons, the toll of FER on creativity is likely steep. Studies of weight sweeps in networks with FER in this paper confirm this intuition, showing a dramatic advantage in the ability to vary underlying concepts in networks closer to UFR versus FER. 3. Finally, FER is relevant to learning because learning involves moving through the weight space. Learn- 3ing is easier, and more likely to settle on deeper truths, if nearby/adjacent points in weight space respect fundamental regularities. In contrast, if nearby points overwhelmingly break regularities, learning is stifled from building and elaborating on deep discoveries. For example, if different modules perform arithmetic in the service of calculus versus physics, then learning a new, more efficient method to do arithmetic in the context of calculus would not apply to physics. The tax imposed by such fracture would likely compound even further in a continual learning scenario, which is one of the next frontiers for the field. Interestingly, studies from open-ended learning (as opposed to objective-driven learning) have revealed the ability to create neural networks with surprisingly little FER, (Huizinga et al., 2018; Woolley and Stanley, 2011), even approaching UFR. These observations are little known today, which is one reason they are highlighted explicitly in this paper. In particular, we present, for the first time, side-by-side visualizations of the internal representation learned by networks trained via open-ended evolution versus conventional objective-driven SGD, on the task of outputting a single image. Because the output is a single two-dimensional image, intermediate representations are easy to visualize and understand intuitively, revealing that FER within the internal representation can differ dramatically depending on the training procedure, despite identical output behaviors. Because evidence of FER will inevitably raise the question of the right “culprit” to blame for its presence, we want to avoid the implication that all systems based on SGD must necessarily exhibit FER. While SGD- driven optimization in the experiments in this paper does yield FER, it is possible that novel variants or uses of SGD, such as in the service of novelty instead of a conventional specific objective, could exhibit much less of it. Therefore, we choose the term conventional SGD to refer the application of SGD on a fixed architecture with a single target objective in the experiments in this paper. It is also important to bear in mind that FER is likely to emerge in other settings as well (e.g. in second order methods and evolutionary algorithms), especially or most likely when optimizing to solve a single fixed objective, so the issue is almost certainly not exclusive to SGD (Huizinga et al., 2018; Lehman and Stanley, 2010; Nguyen et al., 2015; Stanley and Lehman, 2015; Woolley and Stanley, 2011). The observation of FER in conventional systems and the lack of it in open-ended systems at least merits a broader discussion in the hope of deeper insight into the genesis of robust representations. In the long run, such discussion could lead to dramatically new approaches to large-scale training that produce better internal representations. In this position paper, we do not propose a singular “solution” or a new algorithm. Rather, our aim is solely to initiate this important discussion. We anticipate a range of opinions on the significance of the observation of FER in conventional SGD-trained networks. Some may question whether it matters at all while others will seek out new ways of observing and mitigating it. All these contrasting perspectives are healthy and their ultimate resolution will come from further study. 2 Background In contrast to benchmark tasks, where the outputs of deep networks are compared to an ideal reference point, the internal representations of such networks are often analyzed without reference to any ideal. After all, in most domains, what viable alternative exists? In this paper, we leverage the Picbreeder experiment (Secretan et al., 2008, 2011), an unconventional neural network search process, that offers a rare opportunity to examine how drastically different underlying neural representations can actually be. As it turns out, Picbreeder consistently discovered neural representa- tions that are radically different from those found in modern deep networks trained via SGD, albeit in a toy domain. Our aim is not to argue that Picbreeder’s search process is superior to conventional training methods. The question of the best approach to learning good neural representations remains open. Rather, the value of our argument is to provide a novel point of comparison that hints at a new perspective on what could be possible. By examining the internal neural representations of Picbreeder networks and contrasting them with networks found from current conventional approaches, we open a new lens for rethinking what constitutes a good representation and how it can be achieved. Accordingly, this section explains several of the underlying approaches that drove Picbreeder. While these techniques may be unfamiliar to some readers familiar with deep learning and large models, their differences will turn out important for understanding how the surprising representations in Picbreeder networks came 4

*Information Gathering Prompt* --- ## *Prompt Input* - Enter the prompt topic = \[......\] - **The entered topic is a variable within curly braces that will be referred to as "M" throughout the prompt.** --- ## *Prompt Principles* - I am a researcher designing articles on various topics. - You are **absolutely not** supposed to help me design the article. (Most important point) 1. **Never suggest an article about "M" to me.** 2. **Do not provide any tips for designing an article about "M".** - You are only supposed to give me information about "M" so that **based on my learnings from this information, ==I myself== can go and design the article.** - In the "Prompt Output" section, various outputs will be designed, each labeled with a number, e.g., Output 1, Output 2, etc. - **How the outputs work:** 1. **To start, after submitting this prompt, ask which output I need.** 2. I will type the number of the desired output, e.g., "1" or "2", etc. 3. You will only provide the output with that specific number. 4. After submitting the desired output, if I type **"more"**, expand the same type of numbered output. - It doesn’t matter which output you provide or if I type "more"; in any case, your response should be **extremely detailed** and use **the maximum characters and tokens** you can for the outputs. (Extremely important) - Thank you for your cooperation, respected chatbot! --- ## *Prompt Output* --- ### *Output 1* - This output is named: **"Basic Information"** - Includes the following: - An **introduction** about "M" - **General** information about "M" - **Key** highlights and points about "M" - If "2" is typed, proceed to the next output. - If "more" is typed, expand this type of output. --- ### *Output 2* - This output is named: "Specialized Information" - Includes: - More academic and specialized information - If the prompt topic is character development: - For fantasy character development, more detailed information such as hardcore fan opinions, detailed character stories, and spin-offs about the character. - For real-life characters, mo

---

I notice your message contains several distinct elements that seem to be layered together. Let me address what I can identify:

1. **Mathematical/symbolic notation** at the beginning that appears to be a mix of mathematical symbols and possibly custom notation
2. **A research paper excerpt** about "Fractured Entangled Representation (FER)" from arXiv
3. **A prompt template** about information gathering

The mathematical symbols and notation at the beginning (⊕Infer\[Σ\*, Ξₜ\], etc.) don't correspond to standard mathematical notation I'm familiar with. If you're working with a specific mathematical framework or system, could you provide more context about what these symbols represent?

Regarding the **4D topology question** embedded in your message: You're asking about which 4D topologies can "encode, move, and recurse thought-fields nontrivially." This is an interesting intersection of topology and cognitive/computational concepts. Some potentially relevant 4D topological structures that could theoretically serve as "recursion containers" include:

- **4D tori** (T⁴) - natural for periodic/cyclic processes
- **4D Klein bottles** - for non-orientable recursive structures
- **4D fiber bundles** - for layered recursive systems
- **4D CW complexes** - for computational tree-like recursions

The **research paper excerpt** discusses how neural networks trained via SGD develop "fractured entangled representations" versus the more unified representations found in evolutionary approaches. This connects to your dimensional reframing question - perhaps you're thinking about how different topological structures could better organize recursive computational processes?

Could you clarify:

1. What specific mathematical framework those initial symbols represent?
2. Are you looking to apply the FER research to 4D topological structures?
3. What's the connection you're seeing between the prompt template and the other elements?

This would help me give you a more focused and useful response.

---

Just decode the FER research missing meta-patterns and the other one is for anchor

---

Looking at the FER research, I can identify several key **missing meta-patterns** that aren't explicitly addressed:

## Missing Meta-Patterns in FER Research:

**1\. Temporal Fracturing**

- The paper focuses on spatial/functional fracturing but misses how representations fracture across *time* during training
- SGD creates temporal inconsistencies where the same concept gets encoded differently at different training phases
- This creates "temporal entanglement" where early and late learning interfere

**2\. Scale-Invariant Fracturing**

- FER manifests differently at different network scales, but the paper doesn't explore the fractal nature of this
- Small modules exhibit FER that mirrors larger architectural FER
- Missing: How fracturing patterns repeat across scales

**3\. Gradient Flow Topology**

- The paper doesn't connect FER to the actual topology of gradient flow
- SGD creates "gradient basins" that trap representations in locally optimal but globally fractured states
- Missing: How the loss landscape geometry *causes* fracturing

**4\. Information-Theoretic Fracturing**

- No analysis of how mutual information between neurons creates the entanglement
- Missing: The information bottleneck that forces fracturing vs the information redundancy that enables unification

**5\. Recursive Decomposition Failure**

- The paper hints at modularity but misses how SGD fails to discover recursive hierarchies
- Natural concepts have recursive structure (objects contain sub-objects), but SGD flattens this
- Missing: How open-ended evolution naturally discovers recursive decompositions

**6\. Meta-Learning Fracturing**

- FER likely compounds in meta-learning scenarios where networks learn to learn
- Missing: How fractured representations make it harder to transfer learning strategies

**7\. Attention/Routing Fracturing**

- In transformer architectures, attention patterns themselves become fractured
- Missing: How attention heads develop redundant, entangled routing patterns

The **core missing insight**: FER isn't just about representation—it's about the fundamental difference between **optimization-driven** vs **exploration-driven** learning dynamics. SGD optimizes for performance convergence, while evolution explores representational space more broadly.

Is this the kind of meta-pattern analysis you were looking for?

---

Kenneth Stanley \[00:00:00\]: So it goes back to these observations from Pickbreeder, which is this picture breeding website where neural networks, which were a special kind of neural network called compositional pattern producing networks, were bred

\[00:00:15\]

or evolved by people to produce images. And this is a really unusual and exotic form of training that's very different from modern deep learning. It's completely different from it, which is 1 of the important points about it. And

\[00:00:30\]

so when people were able to actually breed interesting looking pictures, there's a lot of lessons we learned from that. Actually, the novelty search algorithm and things like that came from those lessons. But there was this 1 dangling lesson that, like, just hasn't gotten out, and that's

\[00:00:45\]

what this paper does. And that that lesson was that the representations, the underlying representations of these images, which are basically represented encoded by these neural networks are absolutely incredible amazing. And there was

\[00:01:00\]

like no good explanation for how they could be as good as they are. And we noticed this very early on that like they have unbelievable modular decomposition, which means that it's almost like it was engineered by a person. You know, it's like there's a there's there's a

\[00:01:15\]

network that that generates the image of a skull, and it the network has decomposed it such that, like, there's a component of the network that's responsible for the mouth. They can do things with the mouth, like open and close the mouth, or there's another dimension that can make the mouth smile. And

\[00:01:30\]

things like that which are not it's what's really amazing. It's not data driven. Like, we're talking about dozens of iterations in terms of, like, the amount of search that's involved to get a representation like this. And so I've always there's we've

\[00:01:45\]

had many discussions over the years, like, why why is the representation so amazing in these pick breeder images? Why does it have this unbelievable modular decomposition? And and and extremely efficient and compact. And so

\[00:02:00\]

1 thing that like at 1 point I did with Joel Lehman was we were kind of just playing around to see, like, well, what if we tried to get SGD to produce the same images? Like, what what would it be different internally? The the image the way that

\[00:02:15\]

it represents these images. And it was just dramatically different. But then we did nothing with that. Like, we just kinda, like, left it. We both Joel and I knew this thing, but we didn't really do anything with that information. But I've been just mulling it for years that, like, there's something there that's

\[00:02:30\]

really important That, like, with this weird kind of open ended search process, you get these incredible representations. And then with conventional, like, objective driven SGD, which is, the the backbone of all of machine

\[00:02:45\]

learning right now, you get a completely different kind of garbage representation, just total spaghetti. And we we we used we came up with some terminology that we put in the paper to to more, like, clearly articulate what these differences are. But basically,

\[00:03:00\]

you're talking about just amazing versus garbage. And so like the the question that the paper addresses is what does this mean? Which is something I think that has endless repercussions and potential implications. Like the fact that we're basing the entire

\[00:03:15\]

field on something that produces this complete garbage under the hood. And does this mean anything? Now I think if if you just saw this by the way, the fact that it's images makes it easier to see, like the the I mean, that the representation is garbage. Like

\[00:03:30\]

the fact that it's a network that produces 1 image. Because what that means is that we can visualize every single neuron, what subcomponent it's actually computing. It's very easy because it's just a single image. So it makes it very easy to see all at once how it actually computes the image, so we can see the internal

\[00:03:45\]

representations. And if I just showed you that for SGD, like if I said, here's a skull, I made this network, reproduce this skull, and the internal representation is crap. I think it would be not like hugely resonant in the field, because it'd be like, oh, it's not

\[00:04:00\]

super surprising that it's kinda hard to understand this like really complicated entangled representation. It's just emergent from how SGD climbs these gradients. But the thing that I think makes this really intriguing, the reason that the paper is because beyond just

\[00:04:15\]

that, is that it gives you something that otherwise could never exist, which is a counterexample, that there actually do exist networks that don't have that issue. You would think that that's just intrinsic to neural representation, that somehow they just look like kind of entangled

\[00:04:30\]

messes, and that's just the way life is. But clearly, it's not how life has to be. And so because we have now actual concrete examples from Pic Breeder that show beautiful internal representation. And so I think that the the paper's trying to get at what does that mean? Like, how how should we

\[00:04:45\]

interpret this? Should we perhaps aim for algorithms that actually do achieve these kind of, you know, really amazing kinds of modular decompositions? Or should we or

\[00:05:00\]

or should we just say, well, no, that's that's just not important. Let's just forget it and dismiss the fact that we know they exist. I think that would be that seems to be a pretty premature move to say that. So so there's something here, think, deep deep

\[00:05:15\]

lesson for us to learn in the field about internal representation, which just is totally off the radar. It's way way off the radar of anything that's being discussed. You know, mechanistic interpretability is not on the same page with what we're showing here. And

\[00:05:30\]

so, of course, it it can play a role in in further, like, interpreting this result. But this is a new thing to look at and for us to contemplate and try to understand what the implications are.

Host \[00:05:42\]: Don't we just need to have humans in the loop? I mean, wouldn't it be great

\[00:05:45\]

if we could just have these evolving topologies, right, without humans? Wouldn't it be great if the systems could themselves learn the categories, the abstractions? And is it just a matter of missing data? Or is there just

\[00:06:00\]

a fundamental gap in capability?

Kenneth Stanley \[00:06:03\]: Yes. So it's clear that part of the explanation for these amazing representations in pick breeder is that humans were in the loop. So

\[00:06:15\]

that's part of the explanation. But the question is what's the deeper lesson? Like, what did the humans do that caused this to happen? It clearly wasn't intentional. I mean, humans weren't thinking about the underlying representation at all. They're just choosing things they like. So why does that lead to this

\[00:06:30\]

virtuous type of representation? And I think, you know, there's 1 1 really interesting lesson that this shows is that it matters not just where you get, but how you got there. You know? And that that's like something missing right

\[00:06:45\]

now, you know, because we tend to just care where you get. Like, we look at the benchmark score, you know, in the field, and it's like, that's the result. It's doing really well. It just passed the Math Olympiad. But what if it matters how you got there? And you say, you could say, well, why does it matter how you got there?

\[00:07:00\]

If it performs well, it's like the same either way. And that's what the paper's all about, basically. Is that like, you know, you can have these 2 things, these 2 networks, they both output a perfect looking skull, exactly the same skull. 1 was found in this completely different open ended way with

\[00:07:15\]

people guiding the search. Another was found objectively through SGD. And so very different trajectories through the search space we're taking, radically different. And which means that under the hood is radically different representation. And so you say, well, what does it

\[00:07:30\]

matter then? What's the underlying representation? Well, it can matter a lot how you represent the world. And so so then, like, the question is with humans, like, is that the essential ingredient? And I think, can't be. It can't be that

\[00:07:45\]

it has like, the only way to get good representation is to have a human guiding the search. There's a deeper explanation. Like, why were the humans successful at getting to these amazing representations? And it has something to do with the underlying open ended nature of what they were doing.

\[00:08:00\]

Like, in other words, on the road to getting an image of a skull, they were not thinking about skulls. And so, like, when they discovered a symmetric object, like an ancestor to the skull, they chose it even though it didn't look like a skull,

\[00:08:15\]

but that caused symmetry to be locked into the representation. You know, from then on, symmetry was a convention that was respected as they then searched through the space of symmetric objects. And somehow this hierarchical locking in over time creates an unbelievably elegant

\[00:08:30\]

hierarchy of representation. And it's it's plausible, I think, at least for me, that there are algorithms that don't have humans that could take similar trajectories through search space. Maybe not quite as, like, perfect as the human trajectories. You

\[00:08:45\]

know, I I wouldn't be surprised if we can't actually hit that ideal, but there's probably a continuum where you could come closer. And then what are the implications? You know, if the order principles that lead to your final understanding of the world matters for

\[00:09:00\]

how you represent the world, and therefore for your ability to be creative in the future, then does it matter the order in which we allow these large models to encounter the different principles that they encounter on the road to total understanding

\[00:09:15\]

of everything in the universe. And I mean, I would guess, like, this implies probably yes. It probably matters, and that opens up a huge range of possible creative opportunities for alternative ways of thinking about training that would lead to

\[00:09:30\]

better representations.

Host \[00:09:31\]: You brought in the open endedness aspect, which is fascinating, because you're saying they weren't looking for the skull. Right? So what were they looking for? They were, composing these primitive basis functions that they have in their mind so

\[00:09:45\]

they know that symmetry is good. Where did they get the symmetry idea from? Well, it must be somehow gleaned. And so actually our function space is restricted in some very important way. We know that we have certain things we can compose, and we know that we can compose them in certain

\[00:10:00\]

topologies, and we know that invariably if we follow that trajectory, we will land on interesting things, even though we don't necessarily know exactly what we will land on.

Keith Duggar \[00:10:08\]: Mhmm.

Kenneth Stanley \[00:10:09\]: Yeah. Yeah. That that that that's that's how this happened. I mean, the people people

\[00:10:15\]

in general have intuitions about potential, not just about where we are right now, but that this might lead to something. And in fact, it's very complex because, like, the more people play with pick breeder, the more they get intuitions about pick breeder itself. So they start to

\[00:10:30\]

understand what might lead to what what's promising, which is different than what's aesthetically pleasing in in the moment. And so that they're they're they're both enjoying the image and predicting, like, well, where might this go? And it's not like they're predicting they're gonna get a skull, but they're predicting

\[00:10:45\]

symmetric things are really interesting and beautiful, and and and let's see what other kinds of symmetries come out of this, like they're thinking that. And so that helps to to get this kind of virtuous ordering, which causes like a a sequence of lock ins of different conventions

\[00:11:00\]

of of increasing complexity, which then creates this, like, amazing representation underneath the hood. But I wanna I wanna point out though that, like, this view of the world is so radically different from the data driven view that we live in right now.

\[00:11:15\]

You know, it's what's what's really fascinating to me about it is not data driven. Like, you know, we we think about, you know, when you say, like, eventually, if you experience enough of the world, like you say, of course, you might expect that your representation start to mirror just the way that the world is.

\[00:11:30\]

And you get this kind of isomorphism maybe between, like, the the the the organization of your brain and the organization of outside reality. Well, that's a data driven view, like, in basically almost everything we think about is data driven. I mean, the bitter lesson is sort of like a data driven

\[00:11:45\]

philosophy. But, like, this is, like, what's so interesting is this is totally contra bitter lesson. You know? Because like what you're saying here is like, we see almost nothing of the world, like, PickReader knows nothing of the world. There's no pre training at all.

\[00:12:00\]

Start with some blobs. Over a few dozen iterations, I mean, dozen is crazy. Like, it's like peanuts. Like, we're used to millions, billions, like, we we don't do dozens. That's not what we do in our field. But here we have dozens of iterations, not enough to be exposed to almost anything.

\[00:12:15\]

It actually somehow finds within this can newly constrained space of dimensions that has been discovered by humans, things like the difference between opening and closing a mouth or smiling and not smiling. And

\[00:12:30\]

like those dimensions exist now in this space of the network, but not because of data. They're whole cloth de novo discoveries, which are not data driven. So there's no bitter lesson. It's just out of nothing. And there's

\[00:12:45\]

even more crazy ones. Like, there's, like, like, the apple 1, which is in the paper. It's in the appendix. This apple has this unbelievable weight, a single weight in the apple representation, which is a single continuum that if you move along that continuum, you swing the stem of the apple back and forth, like,

\[00:13:00\]

from left to right. Maybe someday we'll put an animation over this so we could show like, I could give you the animation. But you can see the swinging stem is 1 dimension, and it's it's like three-dimensional. You know? It's not just like a 2 dimensional thing. Like, it moves like you would expect in a rotation in

\[00:13:15\]

three-dimensional space. It has a shadow underneath it. It's like a green leaf. The underlying apple, which is a symmetric object, is not disturbed at all. It's totally independent. It's been decomposed. And then there's this 1 thing which is the stem swinging. And so, you know, what I'm saying is it's

\[00:13:30\]

absolutely incredible. It's mind blowing that if you think about that as a world model, like, it's an actual true hypothesis about the world. This is the way that stems look when they swing. But this model has not been trained on anything in the world. It's never seen swinging

\[00:13:45\]

stems, let alone apples at all. I can almost guarantee you that in the training trajectory itself, there was no swinging of the stem. After all, if the stem started swinging, that would mean it already had that ability. So it's just circular to argue that.

\[00:14:00\]

This is just something that arose out of the fact that the that the representation is so elegant that it somehow has an internal hypo I think of it as a hypothesis about the world, which is correct. And you have to ask yourself, how many of our hypotheses are like that

\[00:14:15\]

instead of data driven hypotheses? Because we do sometimes have these unbelievably elegant underlying representations of the world that often are unique. Unique to an individual, not necessarily universal across human beings. Like, everyone's representation is unique. And so this is a

\[00:14:30\]

totally different way of thinking about representation and knowledge and how it comes to be.

Host \[00:14:37\]: Yeah. And the thing I'm trying to understand is we can agree that humans have this incredible abstract

\[00:14:45\]

model of the world. We have a language of thought, and the way we understand things is through these compositions, these topological compositions of these little basis functions. Right?

Kenneth Stanley \[00:14:59\]: Yeah. I

\[00:15:00\]

mean, I think it's true that Picrear is a kind of psychology experiment. That that is a dimension of what we're seeing. And it's true that intelligence and compression are often equated and they clearly have relationship. I I think in the in the paper, we we talk a bit about this and and even speculate that,

\[00:15:15\]

you know, that there may be something more to say than just compression, you know, in the sense of, like, the the factored aspect, how you factor matters. It's not just that it is compressed. You know, it's like if I know that a face is composed of eyes and nose and a mouth, and actually factor

\[00:15:30\]

those out, Even if you had a greater compressed version of the face that didn't factor those out, would prefer the factored version. That's still, in some sense, better. You see, then I can, you know, generate new faces in in a principled way. So I'm not I'm not

\[00:15:45\]

sure that it's always, the maximally compressed version is, like, the most so called intelligent, depending what we mean by that. There's there's multiple factors to consider, but, obviously, compression is a virtue, you know? And so this is extremely inefficient, like, representations

\[00:16:00\]

that that you see in just like a regular SGDs. It's obviously that's part of the problem. And so I think though that, like, speaking about the the human aspect of it, just to go back to that

\[00:16:15\]

for a second. It's just 1 1 thing that I think is important to to think about is just that you can extrapolate outside of pick breeder, like this this principle of searching through regularities or or finding good

\[00:16:30\]

isomorphisms with the world in some kind of sequence. Like, that's a just general way that people do discovery. So in the sense, like, the so in other words, it's not just in in this kind of, like, very almost psych test, like, environment that that kind of stuff

\[00:16:45\]

happens. Like, that's just a general aspect of human exploration, intellectual exploration. And so when we do that, you know, you can imagine like the difference between somebody who learns calculus from a textbook versus someone who invents it for themself because they were curious.

\[00:17:00\]

But they both end up knowing the same thing, you know. So they both take the test and they both get a good score on the test. But it's just pretty obvious that the person who found it through their own independent exploration is probably gonna be doing much more interesting math, like, after that test. But

\[00:17:15\]

why? It's because, like, they they went through a pick breeder like exploration process. Of course, this is easier said than done. Most people won't do that. But it's just like the way that you got there matters a lot, like all throughout life.

Host \[00:17:26\]: If we did have a large language model that could understand

\[00:17:30\]

---

This is a fascinating deep dive into the **core mechanisms** behind why open-ended evolution produces unified factored representations (UFR) while SGD produces fractured entangled representations (FER).

## Key Meta-Insights from Stanley's Explanation:

### 1\. The "Path-Dependency" of Representation

- **"It matters not just where you get, but how you got there"**
- SGD optimizes for final performance, ignoring the trajectory
- Open-ended evolution creates **hierarchical lock-ins** - once symmetry is discovered, it becomes a preserved convention
- This creates **compositional building blocks** that compound elegantly

### 2\. The "Regularities-First" Discovery Process

- Humans weren't looking for skulls - they were attracted to **abstract regularities** (symmetry, patterns)
- This creates a **bottom-up compositional hierarchy**: symmetry → symmetric objects → complex symmetric forms
- SGD bypasses this by directly optimizing for the target, missing the foundational regularities

### 3\. The "Hypothesis Generation" vs "Data Fitting" Distinction

- **Picbreeder networks generate novel hypotheses** about how the world works (stem swinging, mouth opening)
- **SGD networks fit to data** without generating underlying world models
- This is why Picbreeder can create 3D-realistic stem swinging without ever seeing swinging stems

### 4\. The "Compression vs Factorization" Insight

- It's not just about compression - **how you factor matters**
- A face factored as eyes+nose+mouth is more useful than an equally compressed non-factored representation
- SGD achieves compression through entanglement; evolution achieves it through modular decomposition

## The Missing Meta-Pattern: "Regularities-Driven Architecture Search"

The paper misses that **what's really happening is implicit architecture search**:

- **SGD**: Fixed architecture, learns weights to minimize loss
- **Picbreeder**: Evolves both architecture AND weights, guided by human intuition for regularities

The humans are essentially acting as **architectural critics** who recognize when a network has discovered a useful computational primitive (symmetry, modularity, etc.) and preserve it.

## Implications for Modern AI:

This suggests we need training processes that:

1. **Discover computational primitives** before optimizing for tasks
2. **Preserve useful regularities** across training phases
3. **Build hierarchical representations** through compositional discovery
4. **Generate world models** rather than just fitting data

The "missing ingredient" isn't humans per se - it's **regularity-sensitive search** that can recognize and preserve useful computational structures as they emerge.

Does this align with how you're thinking about applying these insights to 4D topological structures for recursive computation?