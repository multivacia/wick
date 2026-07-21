/** Navigation model for I5 application shell — route-driven, screen-agnostic. */

export type NavItemId =
  | "overview"
  | "runs"
  | "readiness"
  | "host-scheduler"
  | "r3e";

export type NavItem = {
  id: NavItemId;
  label: string;
  path: string;
  active: true;
};

export type PlannedNavItem = {
  id: string;
  label: string;
  active: false;
  note: string;
};

export type NavGroup = {
  id: string;
  label: string;
  items: Array<NavItem | PlannedNavItem>;
};

const OVERVIEW: NavItem = {
  id: "overview",
  label: "Visão Geral",
  path: "/overview",
  active: true,
};

const RUNS: NavItem = {
  id: "runs",
  label: "Execuções",
  path: "/future-collection/runs",
  active: true,
};

const READINESS: NavItem = {
  id: "readiness",
  label: "Prontidão",
  path: "/future-collection/readiness",
  active: true,
};

const HOST_SCHEDULER: NavItem = {
  id: "host-scheduler",
  label: "Host e Automação",
  path: "/operations/host-scheduler",
  active: true,
};

const R3E: NavItem = {
  id: "r3e",
  label: "Experimento R3E",
  path: "/experiments/r3e",
  active: true,
};

/** Active MVP routes authorized for I5 / I6 screens. */
export const ACTIVE_NAV_ITEMS: readonly NavItem[] = [
  OVERVIEW,
  RUNS,
  READINESS,
  HOST_SCHEDULER,
  R3E,
];

export const NAV_GROUPS: readonly NavGroup[] = [
  {
    id: "overview-group",
    label: "Operação",
    items: [OVERVIEW],
  },
  {
    id: "future-collection",
    label: "Coleta Futura",
    items: [
      RUNS,
      READINESS,
      {
        id: "collected-data",
        label: "Dados Coletados",
        active: false,
        note: "Planejado — não disponível nesta versão",
      },
    ],
  },
  {
    id: "operations",
    label: "Infraestrutura",
    items: [
      HOST_SCHEDULER,
      {
        id: "backups",
        label: "Backups",
        active: false,
        note: "Planejado — não disponível nesta versão",
      },
      {
        id: "incidents",
        label: "Incidentes",
        active: false,
        note: "Planejado — não disponível nesta versão",
      },
    ],
  },
  {
    id: "experiments",
    label: "Experimentos",
    items: [R3E],
  },
  {
    id: "governance",
    label: "Governança",
    items: [
      {
        id: "backlog",
        label: "Backlog",
        active: false,
        note: "Planejado — não disponível nesta versão",
      },
      {
        id: "approvals",
        label: "Aprovações",
        active: false,
        note: "Planejado — não disponível nesta versão",
      },
      {
        id: "evidence",
        label: "Evidências",
        active: false,
        note: "Planejado — não disponível nesta versão",
      },
    ],
  },
];

export function isActiveNavItem(
  item: NavItem | PlannedNavItem,
): item is NavItem {
  return item.active === true;
}

export type RoutePlaceholderModel = {
  title: string;
  description: string;
  routeId: string;
  statusLabel: string;
};

export const ROUTE_PLACEHOLDERS: Record<string, RoutePlaceholderModel> = {
  "/overview": {
    title: "Visão Geral",
    description:
      "Área reservada para o resumo operacional. O conteúdo da tela ainda não foi implementado.",
    routeId: "/overview",
    statusLabel: "Planejado / não implementado",
  },
  "/future-collection/runs": {
    title: "Execuções",
    description:
      "Área reservada para listar execuções da coleta futura. O conteúdo da tela ainda não foi implementado.",
    routeId: "/future-collection/runs",
    statusLabel: "Planejado / não implementado",
  },
  "/future-collection/readiness": {
    title: "Prontidão",
    description:
      "Área reservada para prontidão operacional da coleta. O conteúdo da tela ainda não foi implementado.",
    routeId: "/future-collection/readiness",
    statusLabel: "Planejado / não implementado",
  },
  "/operations/host-scheduler": {
    title: "Host e Automação",
    description:
      "Área reservada para host e automação. O conteúdo da tela ainda não foi implementado.",
    routeId: "/operations/host-scheduler",
    statusLabel: "Planejado / não implementado",
  },
};

export const NOT_FOUND_PLACEHOLDER: RoutePlaceholderModel = {
  title: "Página não encontrada",
  description:
    "A rota solicitada não existe nesta versão do shell operacional.",
  routeId: "/not-found",
  statusLabel: "Não encontrado",
};
