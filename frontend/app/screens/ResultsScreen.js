import { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  SafeAreaView,
  ScrollView,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { Colors } from '../constants/colors';
import Card from '../components/Card';
import Button from '../components/Button';
import { getResults } from '../api/trips';

export default function ResultsScreen({ navigation, route }) {
  const { tripId } = route.params;
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedDest, setSelectedDest] = useState(0);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const data = await getResults(tripId);
        setResults(data);
      } catch (error) {
        Alert.alert(
          'Error',
          'Could not load results. Make sure all travelers have voted on at least one common destination.'
        );
      } finally {
        setLoading(false);
      }
    };
    fetchResults();
  }, []);

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator color={Colors.primary} size="large" />
        <Text style={styles.loadingText}>Finding best flights...</Text>
      </View>
    );
  }

  if (!results || results.destinations.length === 0) {
    return (
      <View style={styles.centered}>
        <Text style={styles.emptyTitle}>No results yet</Text>
        <Text style={styles.emptySubtitle}>
          Make sure at least 2 travelers have joined and voted on a common destination.
        </Text>
        <View style={styles.backButton}>
          <Button
            title="Go back"
            variant="secondary"
            onPress={() => navigation.goBack()}
          />
        </View>
      </View>
    );
  }

  const destination = results.destinations[selectedDest];

  return (
    <SafeAreaView style={styles.safe}>
      <ScrollView contentContainerStyle={styles.container}>

        {/* Destination tabs */}
        <Text style={styles.sectionLabel}>AGREED DESTINATIONS</Text>
        <ScrollView
          horizontal
          showsHorizontalScrollIndicator={false}
          style={styles.tabScroll}
        >
          {results.destinations.map((dest, index) => (
            <View
              key={dest.destination}
              style={[
                styles.tab,
                selectedDest === index && styles.tabSelected,
              ]}
            >
              <Text
                style={[
                  styles.tabText,
                  selectedDest === index && styles.tabTextSelected,
                ]}
                onPress={() => setSelectedDest(index)}
              >
                {dest.city_name}
              </Text>
            </View>
          ))}
        </ScrollView>

        {/* Destination header */}
        <View style={styles.destHeader}>
          <Text style={styles.destCity}>{destination.city_name}</Text>
          <Text style={styles.destCode}>{destination.destination}</Text>
          <Text style={styles.destVotes}>
            {destination.vote_count} traveler{destination.vote_count !== 1 ? 's' : ''} voted for this
          </Text>
        </View>

        {/* Flight options */}
        <Text style={styles.sectionLabel}>FLIGHT OPTIONS</Text>
        <Text style={styles.optionsHint}>
          Each option picks the best flights for the whole group, not just individuals.
        </Text>

        {destination.options.map((option) => (
          <Card key={option.label} style={styles.optionCard}>

            {/* Option header */}
            <View style={styles.optionHeader}>
              <Text style={styles.optionLabel}>{option.label}</Text>
              <View style={styles.optionBadges}>
                <View style={styles.badge}>
                  <Text style={styles.badgeText}>
                    {option.spread_hours < 1
                      ? `${Math.round(option.spread_hours * 60)}m apart`
                      : `${option.spread_hours.toFixed(1)}h apart`}
                  </Text>
                </View>
                <View style={[styles.badge, styles.badgeCost]}>
                  <Text style={styles.badgeText}>
                    ${option.total_cost.toLocaleString()} total
                  </Text>
                </View>
              </View>
            </View>

            {/* Sync bar */}
            <View style={styles.syncRow}>
              <Text style={styles.syncLabel}>Arrival sync</Text>
              <View style={styles.syncBar}>
                <View
                  style={[
                    styles.syncFill,
                    {
                      width: `${Math.max(5, 100 - option.spread_hours * 5)}%`,
                      backgroundColor:
                        option.spread_hours < 3
                          ? Colors.success
                          : option.spread_hours < 8
                          ? Colors.primary
                          : Colors.error,
                    },
                  ]}
                />
              </View>
            </View>

            {/* Individual flights */}
            <Text style={styles.flightsLabel}>INDIVIDUAL FLIGHTS</Text>
            {option.flights.map((flight, i) => (
              <View key={i} style={styles.flightRow}>
                <View style={styles.flightRoute}>
                  <Text style={styles.flightCode}>
                    {flight.origin} → {flight.destination}
                  </Text>
                  <Text style={styles.flightTime}>
                    Departs {flight.departure}
                  </Text>
                  <Text style={styles.flightTime}>
                    Arrives {flight.arrival}
                  </Text>
                </View>
                <Text style={styles.flightPrice}>
                  ${flight.price_usd.toLocaleString()}
                </Text>
              </View>
            ))}

          </Card>
        ))}

        <View style={styles.backButton}>
          <Button
            title="Back to members"
            variant="secondary"
            onPress={() => navigation.goBack()}
          />
        </View>

      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: {
    flex: 1,
    backgroundColor: Colors.background,
  },
  centered: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 32,
    backgroundColor: Colors.background,
  },
  loadingText: {
    marginTop: 16,
    fontSize: 15,
    color: Colors.textMuted,
  },
  emptyTitle: {
    fontSize: 22,
    fontWeight: '700',
    color: Colors.textDark,
    marginBottom: 8,
    textAlign: 'center',
  },
  emptySubtitle: {
    fontSize: 15,
    color: Colors.textMuted,
    textAlign: 'center',
    lineHeight: 22,
  },
  container: {
    padding: 24,
    paddingBottom: 48,
  },
  sectionLabel: {
    fontSize: 11,
    fontWeight: '700',
    color: Colors.textMuted,
    letterSpacing: 1,
    marginBottom: 12,
  },
  tabScroll: {
    marginBottom: 24,
  },
  tab: {
    paddingVertical: 8,
    paddingHorizontal: 16,
    borderRadius: 20,
    borderWidth: 1,
    borderColor: Colors.border,
    backgroundColor: Colors.surface,
    marginRight: 8,
  },
  tabSelected: {
    backgroundColor: Colors.primary,
    borderColor: Colors.primary,
  },
  tabText: {
    fontSize: 14,
    color: Colors.textDark,
    fontWeight: '500',
  },
  tabTextSelected: {
    color: Colors.white,
  },
  destHeader: {
    marginBottom: 28,
  },
  destCity: {
    fontSize: 30,
    fontWeight: '700',
    color: Colors.textDark,
    letterSpacing: -0.5,
  },
  destCode: {
    fontSize: 15,
    color: Colors.textMuted,
    marginTop: 2,
  },
  destVotes: {
    fontSize: 13,
    color: Colors.primary,
    marginTop: 4,
  },
  optionsHint: {
    fontSize: 13,
    color: Colors.textMuted,
    marginBottom: 16,
    lineHeight: 18,
  },
  optionCard: {
    marginBottom: 16,
  },
  optionHeader: {
    marginBottom: 14,
  },
  optionLabel: {
    fontSize: 17,
    fontWeight: '700',
    color: Colors.textDark,
    marginBottom: 8,
  },
  optionBadges: {
    flexDirection: 'row',
    gap: 8,
  },
  badge: {
    backgroundColor: Colors.primary,
    paddingVertical: 4,
    paddingHorizontal: 10,
    borderRadius: 6,
  },
  badgeCost: {
    backgroundColor: Colors.textMuted,
  },
  badgeText: {
    color: Colors.white,
    fontSize: 12,
    fontWeight: '600',
  },
  syncRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
    marginBottom: 16,
  },
  syncLabel: {
    fontSize: 12,
    color: Colors.textMuted,
    width: 72,
  },
  syncBar: {
    flex: 1,
    height: 6,
    backgroundColor: Colors.border,
    borderRadius: 3,
    overflow: 'hidden',
  },
  syncFill: {
    height: '100%',
    borderRadius: 3,
  },
  flightsLabel: {
    fontSize: 11,
    fontWeight: '700',
    color: Colors.textMuted,
    letterSpacing: 1,
    marginBottom: 10,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: Colors.border,
  },
  flightRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  flightRoute: {
    flex: 1,
    gap: 2,
  },
  flightCode: {
    fontSize: 14,
    fontWeight: '600',
    color: Colors.textDark,
  },
  flightTime: {
    fontSize: 12,
    color: Colors.textMuted,
  },
  flightPrice: {
    fontSize: 15,
    fontWeight: '700',
    color: Colors.primary,
  },
  backButton: {
    marginTop: 24,
  },
});