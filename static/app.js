// COLLECTION / WISHLIST / REVIEWPAGE fragrance searching
$(document).ready(function() {
    // Function to handle click on fragrance option in the dropdown
    $('#searchResults').on('click', 'div', function() {
        var selectedFragrance = $(this).text().trim();
        $('#fragrance_name').val(selectedFragrance);
        $('#fragrance_name_form').submit();
    });

    function performSearch() {
        var nameQuery = $('#fragrance_name').val();
        var houseQuery = $('#fragrance_house').val();

        var url = '';
        var data = {};

        if (nameQuery && houseQuery) {
            url = '/search_fragrances_by_name_and_house';
            data = { name_query: nameQuery, house_query: houseQuery };
        } else if (nameQuery) {
            url = '/search_fragrances_by_name';
            data = { query: nameQuery };
        } else if (houseQuery) {
            url = '/search_fragrances_by_house';
            data = { query: houseQuery };
        } else {
            $('#searchResults').empty();
            return; // If both fields are empty, do nothing
        }

        $.ajax({
            url: url,
            type: 'GET',
            data: data,
            success: function(data) {
                $('#searchResults').empty();
                
                data.sort(function(a, b) {
                    var nameA = a.name.toUpperCase(); // Ignore case
                    var nameB = b.name.toUpperCase(); // Ignore case
                    
                    if (nameA < nameB) {
                        return -1;
                    }
                    if (nameA > nameB) {
                        return 1;
                    }

                    // names must be equal
                    return 0;
                });

                $.each(data, function(index, fragrance) {
                    $('#searchResults').append('<div class=" form fragtext bordered spacing2 fragrance_select">' + fragrance.name + ' by ' + fragrance.house + '</div>');
                });
            }
        });
    }

    $('#fragrance_name, #fragrance_house').on('input', function() {
        performSearch();
    });
});





// REVIEW handling deletion
function confirmDelete(reviewId) {
    const reviewElement = document.getElementById(`review_${reviewId}`);
    reviewElement.innerHTML = `
        <p>Are you sure you want to delete this review?</p>
        <button class="confirm-button" onclick="deleteReview(${reviewId})">Yes</button>
        <button class="confirm-button" onclick="cancelDelete(${reviewId})">No</button>
    `;
}

function deleteReview(reviewId) {
    $.ajax({
        url: '/delete_review',
        type: 'POST',
        data: { review_id: reviewId },
        success: function(response) {
            if (response.success) {
                document.getElementById(`review_${reviewId}`).remove();
            } else {
                alert('Failed to delete review.');
            }
        },
        error: function() {
            alert('Error occurred while deleting review.');
        }
    });
}

function cancelDelete(reviewId) {
    // Reload the page to show the original content
    location.reload();
}





// REVIEW liking
function addLike(review_id, button) {
    $.ajax({
        url: '/like_review',
        type: 'POST',
        data: { review_id: review_id },
        success: function(response) {
            if (response.success) {
                $(button).find('i').toggleClass('far fas');
                $(button).toggleClass('liked');
            } else {
                alert('An error occurred.');
            }
        },
        error: function() {
            alert('ERROR BAD');
        }
    });
}



// REVIEW PAGE rating submit and removal 
function submitRating(fragrance_name, fragrance_house, rating) {
    $.ajax({
        url: '/rate_fragrance',
        type: 'POST',
        data: {
            fragrance_name: fragrance_name,
            fragrance_house: fragrance_house,
            rating: rating
        },
        success: function(response) {
            if (response.success) {
                location.reload();
            } else {
                alert('Failed to add rating.');
            }
        },
        error: function() {
            alert('Error occurred while adding rating.');
        }
    });
}

function removeRating(fragrance_name, fragrance_house) {
    $.ajax({
        url: '/remove_rating',
        type: 'POST',
        data: {
            fragrance_name: fragrance_name,
            fragrance_house: fragrance_house
        },
        success: function(response) {
            if (response.success) {
                location.reload();
            } else {
                alert('Failed to remove rating.');
            }
        },
        error: function() {
            alert('Error occurred while removing rating.');
        }
    });
}


