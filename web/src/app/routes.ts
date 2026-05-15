export type AppRoute = "tonto" | "admin";

export function getRouteFromPathname(pathname: string): AppRoute {
  if (pathname === "/admin") {
    return "admin";
  }

  return "tonto";
}

export function getPathnameForRoute(route: AppRoute) {
  return route === "admin" ? "/admin" : "/";
}
