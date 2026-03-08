Project Idea: "The Interactive Mythos Director"
An AI Creative Director that builds an "Infinite Lore" universe where text, images, and audio are generated in one interleaved stream.

The Experience: A user describes a character (e.g., "A cyberpunk samurai in Neo-Tokyo"). Gemini doesn't just describe them; it returns a formatted markdown response that includes a character portrait (Image Gen), a 30-second backstory (Text), and a "voice memo" from the character (Audio).

Multimodal Edge: Uses Gemini’s native interleaved output. The agent acts as a dungeon master that provides the "visuals" for every turn of the story.

Tech Stack:

Models: Gemini 3.1 Flash (for logic) + Imagen 4/Nano Banana (for image generation) + Veo (for 5-second "cinematic" cutscenes).

Cloud: Google Cloud Storage to host the generated assets.

Mandatory Tech: Utilize interleaved content types in the GenAI SDK.

###

To win the Creative Storyteller category, your project must function as an AI Creative Director that doesn't just "chat," but orchestrates a rich, multimodal stream of content.

Here is the step-by-step roadmap to building "The Interactive Mythos Director."

🛠️ Step 1: Environment & Google Cloud Setup
Since GCP deployment is a mandatory requirement, start here:

Project Initialization: Create a project in the Google Cloud Console and enable the Vertex AI API.

Compute: Use Cloud Run to host your backend. It’s the easiest way to demonstrate a "live" server for the judges.

Storage: Set up a Google Cloud Storage (GCS) bucket. This will act as your "Asset Library" for the images and audio files your agent generates.

🧠 Step 2: The "Brain" (Gemini Logic)
You need to use the Google GenAI SDK with Gemini 2.5 Flash or Gemini 3.1 Flash-Lite.

System Instructions: Define the persona. Tell Gemini:

"You are an Interactive Mythos Director. When a user gives you a prompt, you must provide a narrative, a detailed visual description for image generation, and a script for voiceover."

Interleaved Output: This is the "secret sauce." Your agent should return a single response object containing text, image prompts, and audio cues.

🎨 Step 3: Multimodal Integration (The "Director" Role)
This is where the agent moves beyond text-in/text-out:

Image Generation: Use Imagen 3 (via Vertex AI) to turn the agent's visual descriptions into high-quality illustrations.

Audio Synthesis: Use Google Cloud Text-to-Speech (TTS). Choose a cinematic or "narrator" style voice to read the story segment.

Video (Bonus): Use the Veo model for 5-second "cinematic beats" to bring key moments to life.

The Assembly: Your backend (Python/Node.js) collects these assets and sends a "package" to the frontend.

💻 Step 4: The User Experience (Frontend)
Avoid a boring chat bubble interface. Think "Digital Storybook":

Dynamic Layouts: Use a frontend like React or Next.js.

Auto-Play: When a story segment arrives, the image should fade in, the text should typewriter-scroll, and the audio should play automatically.

Branching Paths: Give the user buttons like "Investigate the cave" or "Confront the guardian" so the story stays interactive.

📹 Step 5: Hackathon Submission Prep
To maximize your score (100% criteria), prepare these specific items:

Architecture Diagram: Draw a flow showing: User UI -> Cloud Run Backend -> Gemini (Logic) -> Imagen/TTS (Media Generation) -> GCS (Storage).

The 4-Minute Demo: Start by stating the problem (e.g., "Static stories are boring"), then show the agent creating a world in real-time. Show, don't just tell.

GCP Proof: Record a quick 30-second clip of your Google Cloud Console Logs showing the API calls happening as you use the app.

link: https://geminiliveagentchallenge.devpost.com/?utm_source=devpost&utm_medium=discord&utm_campaign=geminilive26