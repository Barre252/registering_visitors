function fetchTodayVisits() {
  fetch(API_TODAY_VISITS_URL)
    .then(response => response.json())
    .then(data => {
      const tableBody = document.querySelector("#todaysVisits tbody");
      const modalContainer = document.getElementById("dynamicModals");

      const anyModalOpen = document.querySelector('.modal.show') !== null;

      // Always clear and rebuild the table
      tableBody.innerHTML = "";

      if (!anyModalOpen) {
        // Only clear and rebuild modals if no modal is open
        modalContainer.innerHTML = "";
      }

      if (data.records.length > 0) {
        data.records.forEach(record => {
          // Insert row
          const row = `
            <tr>
              <td class="ps-4 fw-semibold">${record.id}</td>
              <td>${record.full_name}</td>
              <td>${record.phone_number}</td>
              <td>${record.person_to_visit}</td>
              <td>${record.civil_servant}</td>
              <td class="text-end pe-4">
                <button type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#todayViewModal${record.id}">
                  <i class="fa fa-eye"> View</i>
                </button>
              </td>
            </tr>`;
          tableBody.insertAdjacentHTML('beforeend', row);

          if (!anyModalOpen) {
            // Insert modal for each record only if no modal open (to avoid removing open modal)
            const modal = `
              <div class="modal fade" id="todayViewModal${record.id}" tabindex="-1" aria-hidden="true">
                <div class="modal-dialog modal-lg">
                  <div class="modal-content">
                    <div class="modal-header bg-info text-white">
                      <h5 class="modal-title">
                        <i class="fa fa-calendar-day me-2"></i>Today's Visit Details
                      </h5>
                      <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                      <div class="row">
                        <div class="col-md-6">
                          <div class="card mb-3">
                            <div class="card-header bg-light">
                              <h6 class="mb-0">Personal Information</h6>
                            </div>
                            <div class="card-body">
                              <dl class="row mb-0">
                                <dt class="col-sm-4">Full Name:</dt>
                                <dd class="col-sm-8">${record.full_name}</dd>
                                <dt class="col-sm-4">Phone:</dt>
                                <dd class="col-sm-8">${record.phone_number}</dd>
                              </dl>
                            </div>
                          </div>
                        </div>
                        <div class="col-md-6">
                          <div class="card mb-3">
                            <div class="card-header bg-light">
                              <h6 class="mb-0">Visit Information</h6>
                            </div>
                            <div class="card-body">
                              <dl class="row mb-0">
                                <dt class="col-sm-6">Office to Visit:</dt>
                                <dd class="col-sm-6">${record.person_to_visit}</dd>
                                <dt class="col-sm-4">Reason:</dt>
                                <dd class="col-sm-8">${record.visit_reason}</dd>
                                <dt class="col-sm-4">Check in Time:</dt>
                                <dd class="col-sm-8">${record.check_in_date} hours</dd>
                              </dl>
                            </div>
                          </div>
                        </div>
                      </div>
                      <div class="card">
                        <div class="card-header bg-light">
                          <h6 class="mb-0">Timing Information</h6>
                        </div>
                        <div class="card-body">
                          <dl class="row mb-0">
                            <dt class="col-sm-4"> Duration:</dt>
                            <dd class="col-sm-8">${record.hours_to_stay}</dd>
                          </dl>
                        </div>
                      </div>
                    </div>
                    <div class="modal-footer">
                      <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        <i class="fa fa-times me-1"></i> Close
                      </button>
                    </div>
                  </div>
                </div>
              </div>`;
            modalContainer.insertAdjacentHTML('beforeend', modal);
          }
        });
      } else {
        tableBody.innerHTML = `
          <tr>
            <td colspan="5" class="text-center py-4 text-muted">No visits scheduled for today</td>
          </tr>`;
      }
    });
}

// Poll every 10 seconds
setInterval(fetchTodayVisits, 10000);
document.addEventListener('DOMContentLoaded', fetchTodayVisits);
