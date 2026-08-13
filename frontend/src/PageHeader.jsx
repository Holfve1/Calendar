function PageHeader({ title, onAddClick, children }) {
  return (
    <>
      <h1>{title}</h1>
      <div className="controls-row">
        <div className="controls-left">{children}</div>
        <button type="button" onClick={onAddClick}>
          + Add Event
        </button>
      </div>
    </>
  );
}

export default PageHeader;
