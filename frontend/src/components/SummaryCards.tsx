interface SummaryCardsProps {
  latestDate: string;
  commoditiesCount: number;
  regionsCount: number;
  activeAlerts: number;
}

export const SummaryCards = ({
  latestDate,
  commoditiesCount,
  regionsCount,
  activeAlerts,
}: SummaryCardsProps) => {
  const summary = [
    { label: "Latest data", value: latestDate },
    { label: "Commodities", value: commoditiesCount.toString() },
    { label: "Regions", value: regionsCount.toString() },
    { label: "Active alerts", value: activeAlerts.toString() },
  ];

  return (
    <section className="summary-cards">
      {summary.map((card) => (
        <article key={card.label} className="summary-card">
          <p>{card.label}</p>
          <h3>{card.value}</h3>
        </article>
      ))}
    </section>
  );
};
