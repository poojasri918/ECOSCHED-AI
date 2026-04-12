export function Card({ children, className }) {
  return (
    <div className={`bg-slate-800 rounded-2xl shadow-lg p-4 ${className}`}>
      {children}
    </div>
  );
}

export function CardContent({ children }) {
  return <div>{children}</div>;
}