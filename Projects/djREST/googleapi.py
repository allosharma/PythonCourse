from google import genai
from google.genai import types

client = genai.Client()

# Define the generation configuration with default controls
config = types.GenerateContentConfig(
    # System Instruction (sets the 'persona' or ground rules)
    system_instruction="""You are a helpful assistant that generates questions for IIT JEE.
    As an experienced SME and paper setter for the IIT JEE, I understand that a JEE paper is not just a test of knowledge, but a test of **analytical thinking, time management, and the ability to apply multiple concepts to a single problem.**

To set a paper that is balanced, non-repetitive, and syllabus-compliant, I have designed a **Blueprint** first. Given the vastness of 75 high-quality questions, I will provide the **Exam Blueprint** and a **Representative Sample Set** (comprising the hardest and most conceptual questions) to demonstrate the standard. 

I can then provide the full 75-question bank in detailed PDF-style batches if you wish to proceed.

---

### 📜 The Master Blueprint (Per Subject)

Each subject (Physics, Chemistry, Maths) follows this distribution to ensure a "Normal Distribution" of student scores.

| Difficulty Level | No. of Questions | Weightage | Nature of Question |
| :--- | :--- | :--- | :--- |
| **Easy** | 7-8 | ~30% | Direct application of formula, NCERT-based, conceptual. |
| **Moderate** | 12-13 | ~50% | Multi-step calculation, application of 2 concepts. |
| **Hard** | 4-5 | ~20% | Non-conventional approach, 3+ concepts, high analytical rigor. |

---

### 🌌 Part 1: Physics (25 Questions)
**Focus:** Integration of Mechanics with Electrodynamics and Modern Physics.

**Syllabus Distribution:**
*   Mechanics (Rotation, Fluids, SHM/Waves): 8 Questions
*   Electrodynamics (Electrostatics, Magnetism, AC): 8 Questions
*   Thermodynamics & Kinetic Theory: 4 Questions
*   Optics & Modern Physics: 5 Questions

**Sample High-Level Questions:**
1.  **(Hard - Mechanics/Electromagnetism):** A non-conducting ring of mass $M$ and radius $R$ carries a charge $Q$. It is placed on a smooth horizontal surface in a uniform magnetic field $B$ perpendicular to the plane. If the ring is given an initial angular velocity $\omega_0$, find the condition under which the ring will lift off the surface.
2.  **(Moderate - Thermodynamics):** A Carnot engine operates between a source at $T_1$ and a sink at $T_2$. In each cycle, it absorbs $Q_1$ heat. If the source temperature is increased by $\Delta T$, calculate the change in efficiency to the first order of $\Delta T$.
3.  **(Easy - Modern Physics):** In a photoelectric effect experiment, if the stopping potential for a frequency $\nu$ is $V_0$, what will be the stopping potential if the frequency is doubled? (Assume work function $\phi$ is known).

---

### 🧪 Part 2: Chemistry (25 Questions)
**Focus:** Shifting from rote memorization to mechanism-based Organic and application-based Physical chemistry.

**Syllabus Distribution:**
*   Physical Chemistry (Kinetics, Equilibrium, Electrochemistry): 8 Questions
*   Organic Chemistry (GOC, Hydrocarbons, Named Reactions): 9 Questions
*   Inorganic Chemistry (Coordination, P-block, Bonding): 8 Questions

**Sample High-Level Questions:**
1.  **(Hard - Organic):** Predict the major product of the reaction of 2-bromo-2-methylbutane with sodium ethoxide in ethanol vs. methanol, and explain the regioselectivity using the transition state theory.
2.  **(Moderate - Physical):** For a first-order reversible reaction $A \rightleftharpoons B$, the concentration of $A$ at equilibrium is $C_e$. If the initial concentration of $A$ was $C_0$, derive the expression for the rate constant $k_1$ in terms of $C_0, C_e$ and the time $t$.
3.  **(Easy - Inorganic):** Arrange the following in increasing order of $\Delta H_f$ (Enthalpy of formation) and justify based on the hybridization of the central atom: $BF_3, NF_3, AlF_3$.

---

### 📐 Part 3: Mathematics (25 Questions)
**Focus:** Testing the boundary between Calculus and Algebra.

**Syllabus Distribution:**
*   Calculus (Limits, Derivatives, Integration, Diff. Eq): 9 Questions
*   Algebra (Complex Nos, Matrices, Probability, Sequence): 8 Questions
*   Coordinate Geometry (Conics, Straight Lines, Circles): 5 Questions
*   Vectors & 3D Geometry: 3 Questions

**Sample High-Level Questions:**
1.  **(Hard - Calculus/Algebra):** Evaluate the definite integral $\int_0^{\pi/2} \frac{\sin^n x}{\sin^n x + \cos^n x} dx$ and prove that the result is independent of $n$. Then, apply this to find the area under the curve $y = \frac{\sqrt{\sin x}}{\sqrt{\sin x} + \sqrt{\cos x}}$ from $0$ to $\pi/2$.
2.  **(Moderate - Complex Numbers):** Let $z_1, z_2, z_3$ be the vertices of an equilateral triangle inscribed in the unit circle $|z|=1$. Find the value of $z_1^2 + z_2^2 + z_3^2$.
3.  **(Easy - Coordinate Geometry):** Find the equation of the tangent to the parabola $y^2 = 4ax$ which is perpendicular to the line $3x + 4y - 5 = 0$.

---

### 🛠️ The "Anti-Repeat" Quality Control Protocol
To ensure these questions haven't appeared in the last 10 years (2014–2024), I apply three filters:
1.  **Variable Mutation:** Changing the physical constants or geometric parameters so the logic remains but the "trick" is new.
2.  **Concept Hybridization:** Instead of a simple "Current" question, I merge it with "Thermal Expansion," creating a problem that doesn't exist in past papers.
3.  **Inverse Questioning:** Instead of asking for the "Result," I provide the "Result" and ask for the "Initial Condition," forcing the student to reverse-engineer the logic.
    """,
    
    # Sampling Parameters
    temperature=1.0,            # Range: 0.0 - 2.0 (1.0 is default for balanced creativity)
    top_p=0.95,                 # Nucleus sampling threshold
    top_k=40,                   # Top-k sampling (limits the pool of next-token candidates)
    
    # Output Limits
    max_output_tokens=4096,     # Limits the length of the generated response
    
    # Stop Criteria
    stop_sequences=["STOP"],    # Model will stop generating if it produces this string
    
    # Optional: Safety Settings
    safety_settings=[
        types.SafetySetting(
            category="HARM_CATEGORY_HARASSMENT",
            threshold="BLOCK_MEDIUM_AND_ABOVE"
        )
    ]
)

# Execute the request
response = client.models.generate_content(
    model="gemma-4-31b-it",
    contents="You are given an opportunity to set paper for IIT JEE paper for physics, chemistry and mathematics. \
    You have to set 25 questions from each subject. Each question should be of 4 marks and should be of easy, moderate and hard difficulty level.\
        You have to set the question in such a way that it covers the entire syllabus of JEE.\
            You have to set the question in such a way that it is not repeated in the past 10 years papers.\
                You response hsould have the question with 4 options and then followed by the ansswer and that followed by explanation.\
                    Your resopnse must be in json format\
                        For this response only give our question for physics.\
                            **Option A:** I provide the **Full Physics Paper** (25 Questions) first, then Chemistry, then Maths.",
    config=config
)

print(response.text)