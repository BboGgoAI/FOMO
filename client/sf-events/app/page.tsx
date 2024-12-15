export const metadata = {
  title: "SF Events",
  description: "Find events happening in San Francisco",
};

// Define the type for an event
interface Event {
  id: number;
  name: string;
  date: string;
  location: string;
  url: string;
}

async function getEvents(): Promise<Event[]> {
  const res = await fetch("http://127.0.0.1:8000/events", { cache: "no-store" });
  if (!res.ok) {
      throw new Error("Failed to fetch events");
  }
  return res.json();
}

export default async function Home() {
  const events = await getEvents();

  return (
      <div className="container mx-auto px-4">
          <h1 className="text-4xl font-bold text-center my-8">SF Events</h1>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {events.map((event) => (
                  <div key={event.id} className="p-4 border rounded shadow">
                      <h2 className="text-xl font-semibold">{event.name}</h2>
                      <p className="text-gray-600">{event.date}</p>
                      <p className="text-gray-800">{event.location}</p>
                      <a
                          href={event.url}
                          target="_blank"
                          rel="noreferrer"
                          className="text-blue-500 underline"
                      >
                          View Details
                      </a>
                  </div>
              ))}
          </div>
      </div>
  );
}
