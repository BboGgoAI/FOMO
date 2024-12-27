"use client";
import { useRef, useEffect } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

interface Event {
  id: string;
  created_at: string;
  name: string;
  date: string;
  url: string;
  location_brief: string;
  full_address: string;
  latitude: number;
  longitude: number;
}

export default function Home() {
  const mapRef = useRef<mapboxgl.Map>(null);
  const mapContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    async function fetchEvents() {
      const res = await fetch("http://127.0.0.1:8000/events", {
        cache: "no-store",
      });
      if (!res.ok) {
        throw new Error("Failed to fetch events");
      }
      const events = (await res.json()) as Event[];
      console.log(events);

      mapboxgl.accessToken =
        "pk.eyJ1Ijoic2Vob2FuYyIsImEiOiJjbTR1bTI2dGYwbjdtMmtwdXRkNnF6eDNtIn0.MBkdVHMHYExKuOl3gwXUFg";
      mapRef.current = new mapboxgl.Map({
        container: mapContainerRef.current!,
        center: [-122.403844, 37.771597],
        zoom: 15,
      });

      events.forEach((event) => {
        new mapboxgl.Marker()
          .setLngLat([event.longitude, event.latitude])
          .setPopup(
            new mapboxgl.Popup({ offset: 25 }).setHTML(
              `<h1 style="color: black">${event.name}</h1>`,
            ),
          )
          .addTo(mapRef.current!);
      });
    }
    fetchEvents();
    return () => {
      mapRef.current!.remove();
    };
  }, []);

  return (
    <>
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-bold text-center my-8">SF Events</h1>
      </div>
      <div className="mx-auto" id="map-container" ref={mapContainerRef!}></div>
    </>
  );
}
