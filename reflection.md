# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
The system helps owners organize daily tasks, prioritize what's important, and create feasible schedules within available time constraints.
Class owner	manages pet owner data and their pets, class Pet stores pet info and manages its tasks,
class Task represents a care activity with type, priority, duration.Class Schedule creates daily plans, sorts, and filters tasks,class TaskType	enum for valid task categories.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Yes, I changed my design, AI find out the bottleneck that task has no link to a pet, so I add task.pet_id = self.id inside add_task, I add method to Pet class,Pet.add_task and Pet.remove_task.

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
Time constraints stops scheduling when time runs out.Pet owners have busy lives. They need to know if their care tasks fit within their available time. Priority constraints because some tasks are more critical than others.The system ensures important tasks get scheduled first. Time is the biggest constraint since people have limited time. Priority helps decide what's essential.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
I got recommendation to group tasks by time, I adopt this recommendation since it reduced time complexity from O(n²) to O(n), groups are easier to work with.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
