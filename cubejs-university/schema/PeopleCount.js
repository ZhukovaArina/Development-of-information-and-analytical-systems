cube(`PeopleCount`, {
  sql: `SELECT * FROM uni.people_count`,

  measures: {
    total_people: {
      sql: `people_count`,
      type: `sum`,
      title: `Всего людей`
    }
  },

  dimensions: {
    building_id: {
      sql: `building_id`,
      type: `number`,
      title: `Корпус`
    }
  }
});
