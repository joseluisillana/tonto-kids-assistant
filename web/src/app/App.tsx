export function App() {
  return (
    <main className="min-h-screen bg-slate-950 px-6 py-10 text-slate-100">
      <section className="mx-auto flex min-h-[calc(100vh-5rem)] max-w-3xl flex-col justify-center">
        <p className="mb-3 text-sm font-medium uppercase tracking-wide text-cyan-300">
          TONTO Web Validation Client
        </p>
        <h1 className="text-4xl font-semibold tracking-normal text-white sm:text-5xl">
          Hola mundo desde el cliente web.
        </h1>
        <p className="mt-5 max-w-2xl text-lg leading-8 text-slate-300">
          Scaffold inicial listo para integrar CI, previews y futuras pruebas
          del backend sin depender siempre de la Raspberry Pi.
        </p>
      </section>
    </main>
  );
}
